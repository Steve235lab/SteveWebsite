# database.py
# Project Database
# Written by Steve D. J. on 2022/5/10
import time

from pymysql import connect


# user_list: list of User objects
# group_list: list of Group objects
class Database:
    user_list = []
    group_list = []
    history_dict = []

    # 读取数据文件初始化
    def __init__(self):
        self.conn = connect(host='localhost', port=3306, user='root', password='root', database='chatroom',
                            charset='utf8')
        self.cursor = self.conn.cursor()
        # 遍历数据库三个表初始化user_list group_list history_dict
        sql1 = """select * from userchat"""
        self.cursor.execute(sql1)
        users = self.cursor.fetchall()
        for user in users:
            username = user[1]
            password = user[2]
            avatar = user[3]
            email = user[4]
            confirmed = user[5]
            confirm_code = user[6]
            contacts = user[7].split(',')
            origin_users = User(username=username, password=password, avatar=avatar, email=email, confirmed=confirmed,
                                confirm_code=confirm_code, contacts=contacts, invitations='')
            self.user_list.append(origin_users)
        sql2 = """select * from contacts_chat"""
        self.cursor.execute(sql2)
        groups = self.cursor.fetchall()
        for group in groups:
            members = group[1].split(',')
            group_num = group[2]
            group_name = group[3]
            group_avatar = group[5]
            origin_groups = Group(members=members, group_num=group_num, group_name=group_name,
                                  group_avatar=group_avatar)
            self.group_list.append(origin_groups)
        sql3 = """select * from chat_history"""
        self.cursor.execute(sql3)
        histories = self.cursor.fetchall()

        group_num_list = []
        meta_historys = []
        history_dict ={}
        for history in histories:
            group_number = history[1]
            if group_number not in group_num_list:
                group_num_list.append(group_number)
            timestamp = history[2]
            sender = history[3]
            content = history[4]
            meta_history = HistoryMeta(group_num=group_number, sender=sender, content=content, timestamp=timestamp)
            meta_historys.append(meta_history)
        for g_num in group_num_list:
            chat_history = ChatHistory(g_num)
            history_dict[int(g_num)] = chat_history
        for meta in meta_historys:
            history_dict[int(meta.group_num)].history.append(meta)
        self.history_dict = history_dict

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    # 将对象写入数据文件
    def save_user(self, user):
        username = user.username
        password = user.password
        avatar = user.avatar
        contacts_list = user.contacts
        contacts = ''
        if len(contacts_list) > 0:
            for contact in contacts_list:
                contacts += contact + ','
            contacts = contacts[:-1]
        else:
            contacts = 'None'
        email = user.email
        confirmed = user.confirmed
        confirm_code = user.confirm_code
        sql = """insert into userchat values (0,"%s","%s","%s","%s","%s","%s","%s",0)""" % (
            username, password, avatar, email,
            confirmed, confirm_code, contacts)
        self.cursor.execute(sql)
        self.conn.commit()

    # 写入group
    def save_group(self, group):
        members_str = ''
        if len(group.members) > 0:
            for member in group.members:
                members_str += member + ','
            members_str = members_str[:-1]
        else:
            members_str = 'None'
        group_num = group.group_num
        group_name = group.group_name
        group_avatar = group.group_avatar
        sql = """insert into contacts_chat values (0,"%s","%s","%s",0,"%s")""" % (
            members_str, group_num, group_name, group_avatar)
        self.cursor.execute(sql)
        self.conn.commit()

    # 写入history
    def save_history(self, meta):
        group_num = meta.group_num
        time = meta.timestamp
        sender = meta.sender
        content = meta.content
        sql = """insert into chat_history values (0,"%s","%s","%s","%s")""" % (group_num, time, sender, content)
        self.cursor.execute(sql)
        self.conn.commit()

    # 添加新用户
    # new_user: User Object
    def add_user(self, new_user):
        self.user_list.append(new_user)
        self.save_user(new_user)

    # 查找指定用户在用户列表中的序号
    # username: str
    # 多用户同时访问时可能存在安全隐患
    def get_user_index(self, username):
        for i in range(len(self.user_list)):
            if username == self.user_list[i].username:
                return i
        # 没找到返回-1
        return -1

    # 用户覆盖写入
    # changed_user: User Object
    def rewrite_user(self, changed_user):
        re_name = changed_user.username
        re_password = changed_user.password
        re_avatar = changed_user.avatar
        re_email = changed_user.email
        re_confirmed = changed_user.confirmed
        re_confirm_code = changed_user.confirm_code
        contacts_list = changed_user.contacts
        contacts = ''
        if len(contacts_list) > 0:
            for contact in contacts_list:
                contacts += contact + ','
            contacts = contacts[:-1]
        else:
            contacts = 'None'
        sql = """update userchat set username = ('%s'),password = ('%s'), avatar = ('%s'),
                 email = ('%s'),confirmed = ('%s'),confirm_code = ('%s'),contact = ('%s') where username = ('%s') """ % (
        re_name, re_password,
        re_avatar, re_email, re_confirmed, re_confirm_code, contacts, re_name)
        self.cursor.execute(sql)
        self.conn.commit()

    # 修改现有用户
    # changed_user: User Object
    def change_user_info(self, changed_user):
        index = self.get_user_index(changed_user.username)
        self.user_list[index] = changed_user
        self.rewrite_user(changed_user)

    # 移除用户
    # username: str
    # 逻辑删除
    def remove_user(self, username):
        sql = """update userchat set is_delete=1 where username = ("%s")""" % username
        self.cursor.execute(sql)
        self.conn.commit()

    # 通过username查找用户对象
    # username: str
    # return User Object
    def get_user_with_username(self, username):
        for user in self.user_list:
            if username == user.username:
                return user
        # 没找到返回Void用户
        user = User(username='Void', password='Void', avatar='Void', email='Void', confirmed='no',
                    confirm_code='Void', contacts=['Void'], invitations=[])
        return user

    # 添加新的聊天群组
    # new_group: Group Object
    def add_group(self, new_group):
        self.group_list.append(new_group)
        self.save_group(new_group)

    # 移除聊天群组
    # group_num: int
    def remove_group(self, group_num):
        sql = """update contacts_chat set is_delete=1 where group_num = ("%d")""" % group_num
        self.cursor.execute(sql)
        self.conn.commit()

    # 通过group_num查找聊天群组对象
    # group_num: int
    # return Group Object
    def get_group_with_group_num(self, group_num):
        for group in self.group_list:
            if group_num == group.group_num:
                return group
        # 没找到返回组号为-1的组
        group = Group(members=[], group_num=-1, group_name='Void')
        return group

    # 添加新的历史记录
    # new_history:HistoryMeta Object
    def add_history(self, new_history):
        self.history_dict.append(new_history)
        self.save_history()

    # 通过group_num查找历史记录
    def get_history_with_group_num(self, group_num):
        chat_history = self.history_dict.get(int(group_num))
        if chat_history is not None:
            return chat_history
        else:
            chat_history = ChatHistory(group_num=-1)
            return chat_history

    # 将验证码关联到对应的用户
    # username: str
    # confirm_code: str
    def set_confirm_code(self, username, confirm_code):
        for i in range(len(self.user_list)):
            if username == self.user_list[i].username:
                self.user_list[i].confirm_code = confirm_code
                self.rewrite_user(self.user_list[i])
                # print("已将验证码关联到用户")

    # 通过用户名查找密码
    # username: str
    def get_user_password(self, username):
        user_found_flag = 0
        for i in range(len(self.user_list)):
            if username == self.user_list[i].username:
                user_found_flag = 1
                return self.user_list[i].password
        if user_found_flag == 0:
            return "User not registered!"

    # 通过用户名查找验证码
    # username: str
    def get_confirm_code(self, username):
        for i in range(len(self.user_list)):
            if username == self.user_list[i].username:
                return self.user_list[i].confirm_code


# 用户
class User:
    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.avatar = kwargs['avatar']
        self.contacts = kwargs['contacts']  # 联系人列表，每个元素为一个group_num
        self.invitations = kwargs['invitations']  # 邀请列表
        self.email = kwargs['email']
        self.confirmed = kwargs['confirmed']  # 邮箱验证通过标记
        self.confirm_code = kwargs['confirm_code']  # 发给用户的邮箱验证码


# 邀请
# 包括：好友邀请、加群申请和入群邀请
class Invitation:
    def __init__(self, **kwargs):
        self.type = kwargs['type']
        self.receiver = kwargs['receiver']
        self.sender = kwargs['sender']


# 群组
# 广义群组，group_num为唯一标识。
class Group:
    # 构造函数
    # members: list of usernames
    # group_num: int
    # group_name: str
    def __init__(self, members, group_num, group_name, group_avatar='/static/avatars/Judy.JPG'):
        self.members = members
        self.group_num = group_num
        self.group_name = group_name
        self.group_avatar = group_avatar

    # 添加成员
    # username: str
    def add_member(self, username):
        if username not in self.members:
            self.members.append(username)
            print("已将用户" + username + "添加至群组" + self.group_name)
        else:
            print("用户" + username + "已经在群组" + self.group_name + "中，不可重复添加。")

    # 删除成员
    # username: str
    def remove_member(self, username):
        if username in self.members:
            self.members.remove(username)
            print("已将用户" + username + "从群组" + self.group_name + "中移除")
        else:
            print("要删除的用户" + username + "不在群组" + self.group_name + "中")


# 聊天记录，与Group对象绑定
class ChatHistory:
    # 构造函数
    # 读取数据文件初始化对象
    # group_num: int
    # history: list of HistoryMeta objects
    def __init__(self, group_num):
        self.group_num = group_num
        self.history = []

    # 向聊天记录中添加一条新消息
    def add_history(self, sender, content):
        new_history = HistoryMeta(self.group_num, sender, content)
        self.history.append(new_history)


# 聊天记录元，每个对象包含一条历史消息
class HistoryMeta:
    # 构造函数
    # group_num: 所属组号 int
    # sender: 发信人用户名 str
    # content: 消息原文 str
    def __init__(self, group_num, sender, content, timestamp=0):
        self.group_num = group_num
        if timestamp == 0:
            self.timestamp = int(time.mktime(time.localtime(time.time())))
        else:
            self.timestamp = timestamp
        self.sender = sender
        self.content = content

    # 格式化为字符串
    def format_str(self):
        history_meta_str = self.timestamp + ',' + self.sender + ','

        # 将content中可能存在的'/'用timestamp替代
        temp_content = self.content
        # content中含有'/'
        if temp_content.find('/') != -1:
            temp_content.replace('/', self.timestamp)

        history_meta_str += temp_content

        return history_meta_str


# 创建全局数据对象
DATABASE = Database()
