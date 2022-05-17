from chat_websocket.database import User, Group

g_1 = Group(['user1', 'user2'], 114514, 'g_1')

new_user = User(username='Steve', password='114514', avatar='../static/avatars/Judy.JPG', contacts=[g_1],
                invitations=[], email='email.com', confirmed='no', confirm_code='None')

print(new_user.contacts[0].group_num)
