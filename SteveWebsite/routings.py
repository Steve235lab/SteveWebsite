# routings.py
# 实现websocket请求的路由，相当于http中的urls
# Written on 2022/4/2 by Steve D. J.
# Based on the video course
from django.urls import re_path
from chat_websocket import consumers

websocket_urlpatterns = [
    # re_path(r'ws/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws_chat_room/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws_sign_up/', consumers.SignUpConsumer.as_asgi()),
    re_path(r'ws_sign_in/', consumers.SignInConsumer.as_asgi()),
    re_path(r'ws_cfm_eml/(?P<username>\w+)/$', consumers.CfmEmlConsumer.as_asgi()),
    re_path(r'ws_add_contact/(?P<username>\w+)/$', consumers.AddContactConsumer.as_asgi()),
]
