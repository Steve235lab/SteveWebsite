from django.urls import path
from chat_websocket import views

urlpatterns = [
    path('', views.sign_up),
    path('sign_up/', views.sign_up),
    path('email_confirm/', views.email_confirm),
    path('sign_in/', views.sign_in),
    path('chatroom/', views.chat_room),
    path('update_info/', views.update_info),
    path('add_contact/', views.add_contact),
]
