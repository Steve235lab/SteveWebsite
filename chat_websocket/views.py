from django.shortcuts import render, HttpResponse
from .database import DATABASE


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
    if username in DATABASE.users_signed_in:
        return render(request, 'chat_room.htm', {"username": username})
    else:
        return render(request, 'session_expired.htm', {"username": username})


def update_info(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        user = DATABASE.get_user_with_username(username)
        email = user.email
        avatar = user.avatar.split('/')[-1]
        return render(request, 'update_info.htm', {"username": username, 'email': email, 'avatar': avatar})
    if request.method == 'POST':
        img = request.FILES.get('photo')
        username = request.GET.get('username')
        email = request.POST.get('email')
        if img is not None:
            file_name = img.name
            suffix_name = file_name.split('.')[-1]
            # print(username)
            # print(file_name)
            avatar_path = './static/avatars/' + username + '.' + suffix_name
            f = open(avatar_path, 'wb')
            f.close()
            with open(avatar_path, 'wb') as avatar_file:
                for part in img.chunks():
                    avatar_file.write(part)
                    avatar_file.flush()
            DATABASE.user_list[DATABASE.get_user_index(username)].avatar = avatar_path
        if email is not None:
            DATABASE.user_list[DATABASE.get_user_index(username)].email = email
        DATABASE.rewrite_user(DATABASE.get_user_with_username(username))
        email = DATABASE.get_user_with_username(username).email
        avatar = DATABASE.get_user_with_username(username).avatar.split('/')[-1]
        return render(request, 'update_info.htm', {"username": username, 'email': email, 'avatar': avatar})


def add_contact(request):
    username = request.GET.get('username')
    return render(request, 'add_contact.htm', {"username": username})

