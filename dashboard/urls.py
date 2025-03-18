from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('weather/', views.weather_data, name='weather_data'),
    path('flights/', views.flight_data, name='flight_data'),
]
