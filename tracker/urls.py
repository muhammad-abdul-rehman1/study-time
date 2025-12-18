from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start/', views.start_study, name='start_study'),
    path('stop/', views.stop_study, name='stop_study'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('history/', views.history, name='history'),
]
