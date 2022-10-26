"""SteveWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views as home_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home),
    path('home/', home_views.home),
    path('poll/', include('chat_polling.urls')),
    path('websocket/', include('chat_websocket.urls')),
    # path(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico')),
    path('try_pyscript/', include('try_pyscript.urls')),
    path('markdown_reader/', include('markdown_reader.urls')),
    path('video_player/', include('video_player.urls')),
    path('speech_compressor/', include('speech_compressor.urls')),
]
