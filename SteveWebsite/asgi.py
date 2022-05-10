"""
ASGI config for SteveWebsite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from SteveWebsite import routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SteveWebsite.settings')

# application = get_asgi_application()

# 支持http和websocket
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(routings.websocket_urlpatterns),
})
