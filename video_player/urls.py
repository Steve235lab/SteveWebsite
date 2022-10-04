from django.urls import path
from video_player import views

urlpatterns = [
    path('', views.render_page),
    path('play_video/', views.stream_video),
]
