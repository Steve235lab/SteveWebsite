from django.urls import path
from speech_compressor import views

urlpatterns = [
    path('', views.render_page),
]
