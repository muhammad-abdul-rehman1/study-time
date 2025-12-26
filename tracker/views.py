from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import StudySession

from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    active_session = StudySession.objects.filter(user=request.user, end_time__isnull=True).first()
    
    today = timezone.now().date()
    # Calculate today's total time
    sessions_today = StudySession.objects.filter(user=request.user, start_time__date=today, end_time__isnull=False)
    
    total_duration = timedelta()
    for session in sessions_today:
        total_duration += session.duration
        
    # Add active session duration up to now if needed, but requirements say "Total study time for today" usually implies finished or current.
    # Let's include active session current duration for better UX
    if active_session:
        total_duration += (timezone.now() - active_session.start_time)

    # Format rough hours/minutes
    total_seconds = int(total_duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    context = {
        'active_session': active_session,
        'total_hours': hours,
        'total_minutes': minutes,
        'is_studying': active_session is not None,
    }
    return render(request, 'dashboard.html', context)

@login_required
def start_study(request):
    if request.method == 'POST':
        # Check if already studying
        active = StudySession.objects.filter(user=request.user, end_time__isnull=True).exists()
        if not active:
            StudySession.objects.create(user=request.user)
    return redirect('dashboard')

@login_required
def stop_study(request):
    active_session = StudySession.objects.filter(user=request.user, end_time__isnull=True).first()
    if active_session:
        active_session.end_time = timezone.now()
        active_session.save()
    return redirect('dashboard')

@login_required
def leaderboard(request):
    today = timezone.now().date()
    users = User.objects.all()
    leaderboard_data = []

    for u in users:
        sessions = StudySession.objects.filter(user=u, start_time__date=today, end_time__isnull=False)
        total = timedelta()
        for s in sessions:
            total += s.duration
            
        # Add active session time
        active = StudySession.objects.filter(user=u, end_time__isnull=True).first()
        if active:
             total += (timezone.now() - active.start_time)
             
        total_seconds = int(total.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if total_seconds > 0: # Only show users who studied
            leaderboard_data.append({
                'user': u,
                'total_seconds': total_seconds,
                'hours': hours,
                'minutes': minutes
            })
    
    # Sort by total time desc
    leaderboard_data.sort(key=lambda x: x['total_seconds'], reverse=True)
    
    return render(request, 'leaderboard.html', {'leaderboard': leaderboard_data})

@login_required
def history(request):
    sessions = StudySession.objects.filter(user=request.user).order_by('-start_time')
    history_data = {}
    
    for s in sessions:
        date = s.start_time.date()
        if date not in history_data:
            history_data[date] = {'sessions': [], 'duration': timedelta()}
        
        history_data[date]['sessions'].append(s)
        history_data[date]['duration'] += s.duration
        
    # Format times
    formatted_history = {}
    for date, data in history_data.items():
        total_seconds = int(data['duration'].total_seconds())
        formatted_history[date] = {
            'sessions': data['sessions'],
            'hours': total_seconds // 3600,
            'minutes': (total_seconds % 3600) // 60
        }
        
    return render(request, 'history.html', {'history': formatted_history})

# --- Pomodoro & Study Together Views ---

import json
from django.http import JsonResponse
import secrets
from .models import StudyRoom, PomodoroSession

@login_required
def study_room(request, room_code):
    try:
        room = StudyRoom.objects.get(room_code=room_code, is_active=True)
        if request.user != room.created_by and request.user != room.partner:
             return redirect('dashboard')
        
        context = {
            'room': room,
            'is_creator': request.user == room.created_by,
        }
        return render(request, 'study_room.html', context)
    except StudyRoom.DoesNotExist:
        return redirect('dashboard')

@login_required
def create_room(request):
    if request.method == 'POST':
        # Deactivate previous active rooms created by user
        StudyRoom.objects.filter(created_by=request.user, is_active=True).update(is_active=False)
        
        # Generate unique code
        while True:
            code = secrets.token_hex(3).upper()
            if not StudyRoom.objects.filter(room_code=code).exists():
                break
        
        room = StudyRoom.objects.create(created_by=request.user, room_code=code)
        return redirect('study_room', room_code=room.room_code)
    return redirect('dashboard')

@login_required
def join_room(request):
    if request.method == 'POST':
        code = request.POST.get('room_code')
        try:
            room = StudyRoom.objects.get(room_code=code, is_active=True)
            if room.partner and room.partner != request.user:
                return redirect('dashboard') # Room full
            
            room.partner = request.user
            room.save()
            return redirect('study_room', room_code=room.room_code)
        except StudyRoom.DoesNotExist:
            pass # Handle invalid code error if needed
    return redirect('dashboard')

@login_required
def pomodoro_action(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        room_code = data.get('room_code')
        
        response_data = {'status': 'success'}
        
        # Handle Room Action
        if room_code:
            try:
                room = StudyRoom.objects.get(room_code=room_code, is_active=True)
                # Verify user permission
                if request.user not in [room.created_by, room.partner]:
                    return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
                
                if action == 'start':
                    phase = data.get('phase', 'study')
                    duration = data.get('duration', 25) # Get custom duration
                    room.timer_status = 'running'
                    room.timer_phase = phase
                    room.timer_duration = duration
                    room.timer_start_time = timezone.now()
                    room.elapsed_time = timedelta(0)
                    room.paused_at = None
                    room.save()

                elif action == 'pause':
                    if room.timer_status == 'running':
                        room.timer_status = 'paused'
                        room.paused_at = timezone.now()
                        room.elapsed_time += (timezone.now() - room.timer_start_time)
                        room.save()

                elif action == 'resume':
                    if room.timer_status == 'paused':
                        room.timer_status = 'running'
                        room.timer_start_time = timezone.now()
                        room.paused_at = None
                        room.save()

                elif action == 'stop':
                    room.timer_status = 'stopped'
                    room.timer_start_time = None
                    room.elapsed_time = timedelta(0)
                    room.paused_at = None
                    room.save()
                
                elif action == 'complete':
                     # Validated by client, but we should double check logic. 
                     # For now, trust client trigger to save the session.
                     phase = room.timer_phase
                     if phase == 'study':
                         # Create StudySession for BOTH users if applicable
                         users_to_credit = [room.created_by]
                         if room.partner:
                             users_to_credit.append(room.partner)
                         
                         duration = timedelta(minutes=room.timer_duration) # Use stored duration
                         
                         # For Leaderboard/StudySession model:
                         for u in users_to_credit:
                             StudySession.objects.create(
                                 user=u, 
                                 start_time=timezone.now() - duration, 
                                 end_time=timezone.now()
                             )
                             
                         # Create Pomodoro History
                         for u in users_to_credit:
                             PomodoroSession.objects.create(
                                 user=u,
                                 start_time=timezone.now() - duration,
                                 end_time=timezone.now(),
                                 phase='study',
                                 is_completed=True,
                                 room=room
                             )
                             
                     room.timer_status = 'stopped'
                     room.save()

            except StudyRoom.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)
        
        return JsonResponse(response_data)
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def room_sync(request, room_code):
    try:
        room = StudyRoom.objects.get(room_code=room_code, is_active=True)
        
        # Calculate current elapsed time based on state
        current_elapsed = room.elapsed_time
        if room.timer_status == 'running' and room.timer_start_time:
            current_elapsed += (timezone.now() - room.timer_start_time)
            
        # Determine who the partner is relative to the current user
        if request.user == room.created_by:
            partner_name = room.partner.username if room.partner else None
            partner_joined = room.partner is not None
        else:
            partner_name = room.created_by.username
            partner_joined = True # If I'm the partner, the "partner" (creator) is obviously there

        data = {
            'status': room.timer_status,
            'phase': room.timer_phase,
            'elapsed_seconds': current_elapsed.total_seconds(),
            'timer_duration': room.timer_duration,
            'partner_joined': partner_joined,
            'partner_name': partner_name
        }
        return JsonResponse(data)
    except StudyRoom.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)
