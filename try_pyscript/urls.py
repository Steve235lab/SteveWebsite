from django.urls import path
from try_pyscript import views


urlpatterns = [
    path('', views.repl_terminal),
]