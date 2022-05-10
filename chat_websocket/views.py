from django.shortcuts import render


def sign_in(request):
    return render(request, 'sign_in.htm')


def sign_up(request):
    return render(request, 'sign_up.htm')


def email_confirm(request):
    # http://42.192.44.52/websocket/email_confirm/?username=Steve
    username = request.GET.get('username')
    return render(request, 'email_confirm.htm', {"username": username})


def chat_room(request):
    # http://42.192.44.52/websocket/chatroom/?username=Steve
    username = request.GET.get('username')
    return render(request, 'chat_room.htm', {"username": username})


