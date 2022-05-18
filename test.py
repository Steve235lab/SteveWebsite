from chat_websocket.database import User, Group,Database,ChatHistory,HistoryMeta

g_1 = Group(['起飞','降落'], 12581, 'g_1')

new_user = User(username='小李', password='114514', avatar='../static/avatars/Judy.JPG', contacts='110',
                invitations=[], email='email.com', confirmed='no', confirm_code='None')

history = HistoryMeta(group_num='12581',sender='校长',content='开除')
room1 = Database()
name="小李"
#room1.add_user(new_user)
#room1.add_group(g_1)
#room1.get_user_with_username(name)
#room1.get_group_with_group_num(12581)
#room1.remove_user(name)
#room1.remove_group(12581)
#room1.add_history(history)
#room1.get_history_with_group_num(12581)



