from chat_websocket.database import User, Group, Database, ChatHistory, HistoryMeta, DATABASE

#
# g_2 = Group(members= ['1', '2'], group_num = 12345, group_name='g_1', group_avatar='')
#
# new_user = User(username='小z', password='114514', avatar='../static/avatars/A1.JPG', contacts=['110'],invitations=[], email='email.com', confirmed='no', confirm_code='None')
user1 = User(username='user1', password='321', avatar='../static/avatars/A1.JPG', contacts=[75, 76], invitations=[], email='haha',
             confirmed='yes', confirm_code='no')
user2 = User(username='user2', password='123', avatar='../static/avatars/A1.JPG', contacts=[75, 76], invitations=[], email='hehe',
             confirmed='yes', confirm_code='no')
user3 = User(username='user3', password='123321', avatar='../static/avatars/A1.JPG', contacts=[76], invitations=[], email='gg',
             confirmed='yes', confirm_code='no')
group_private = Group(members=['user1', 'user2'], group_num=75, group_name='user1、user2', group_avatar='../static/avatars/QQ.jpg')
group_public = Group(members=['user1', 'user2', 'user3'], group_num=76, group_name='三人群聊测试', group_avatar='../static/avatars/QQ.jpg')
# history_75 = ChatHistory(75)
# history_76 = ChatHistory(76)

# DATABASE.add_user(user1)
# DATABASE.add_user(user2)
# DATABASE.add_user(user3)
# DATABASE.add_group(group_private)
# DATABASE.add_group(group_public)
# DATABASE.get_user_with_username('a')
# history = HistoryMeta(group_num='12581', sender='校长', content='开除')
# room1 = Database()
# name="野兽先辈"
# room1.add_user(new_user)
# room1.add_group(g_1)
# user = room1.get_user_with_username(name)
# print(user.contacts)
# group = room1.get_group_with_group_num(114514)
# room1.remove_user(name)
# group = room1.remove_group(114514)
# print(group.group_avatar)
# room1.add_history(history)
# room1.get_history_with_group_num(12581)
# room1.rewrite_group(g_2)
# DATABASE.add_history(history_75)
# DATABASE.add_history(history_76)

# history_meta = HistoryMeta(75, 'user1', '后台添加的聊天记录')
# DATABASE.save_history(history_meta)

# user1 = DATABASE.get_user_with_username('user1')
# user1.avatar = '/static/avatars/A1.png'
# DATABASE.rewrite_user(user1)

dictionary = DATABASE.history_dict
print(dictionary)
