from django.urls import path
from chat_polling import views

urlpatterns = [
    path('', views.poll),
    path('send/msg/', views.send_msg),
    path('get/msg/', views.get_msg),
]
