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
