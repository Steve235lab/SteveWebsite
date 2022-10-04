from django.urls import path
from markdown_reader import views

urlpatterns = [
    path('', views.markdown_reader),
]
