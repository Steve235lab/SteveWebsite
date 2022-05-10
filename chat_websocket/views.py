from django.shortcuts import render


def sign_in(request):
    return render(request, 'sign_in.htm')


def sign_up(request):
    return render(request, 'sign_up.htm')


def email_confirm(request):
    # http://42.192.44.52/websocket/email_confirm/?username=Steve
    username = request.GET.get('username')
    return render(request, 'email_confirm.htm', {"username": username})


def websocket(request):
    # http://42.192.44.52/websocket/?group=114514
    group_num = request.GET.get('group')
    return render(request, 'websocket.htm', {"group_num": group_num})


