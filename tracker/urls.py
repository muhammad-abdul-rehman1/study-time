from django.urls import path
from . import views
from allauth.account.views import SignupView

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start/', views.start_study, name='start_study'),
    path('stop/', views.stop_study, name='stop_study'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    path('history/', views.history, name='history'),
    path('create-room/', views.create_room, name='create_room'),
    path('join-room/', views.join_room, name='join_room'),
    path('room/<str:room_code>/', views.study_room, name='study_room'),
    path('api/pomodoro/', views.pomodoro_action, name='pomodoro_action'),
    path('api/room/<str:room_code>/sync/', views.room_sync, name='room_sync'),
]
