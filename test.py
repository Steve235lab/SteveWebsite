from chat_websocket.database import User, Group, Database, ChatHistory, HistoryMeta
#
#g_2 = Group(members= ['1', '2'], group_num = 12345, group_name='g_1', group_avatar='')
#
new_user = User(username='小z', password='11451411111111111111', avatar='../static/avatars/A1.JPG', contacts=['110'],
                invitations=[], email='email.com', confirmed='no', confirm_code='None')

# history = HistoryMeta(group_num='12581', sender='校长', content='开除')
#room1 = Database()
# name="野兽先辈"
#room1.add_user(new_user)
#room1.add_group(g_1)
#user = room1.get_user_with_username(name)
#print(user.contacts)
#group = room1.get_group_with_group_num(114514)
#room1.remove_user(name)
#group = room1.remove_group(114514)
#print(group.group_avatar)
#room1.add_history(history)
#room1.get_history_with_group_num(12581)
#room1.rewrite_group(g_2)



