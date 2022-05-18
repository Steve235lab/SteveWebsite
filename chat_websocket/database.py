# database.py
# Project Database
# Written by Steve D. J. on 2022/5/10
import time

from pymysql import connect

# user_list: liat of User objects
# group_list: list of Group objects
class Database:
    user_list = []
    group_list = []
    history_list = []

    # 读取数据文件初始化
    def __init__(self):
        self.conn = connect(host='localhost',port=3306,user='root',password='root',database='chatroom',charset='utf8')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    # 将对象写入数据文件
    def save_user(self):
        for user in self.user_list:
            username = user.username
            password = user.password
            avatar = user.avatar
            contacts = user.contacts
            email = user.email
            confirmed = user.confirmed
            confirm_code = user.confirm_code
            sql = """insert into userchat values (0,"%s","%s","%s","%s","%s","%s","%s",0)""" % (username,password,avatar,email,
                                                                                              confirmed,confirm_code,contacts)
            self.cursor.execute(sql)
            self.conn.commit()

    # 写入group
    def save_group(self):
        for group in self.group_list:
            members = group.members
            group_num = group.group_num
            group_name = group.group_name
            sql = """insert into contacts_chat values (0,"%s","%s","%s",0)""" % (members,group_num,group_name)
            self.cursor.execute(sql)
            self.conn.commit()

    #写入history
    def save_history(self):
        for history in self.history_list:
            group_num = history.group_num
            time = history.timestamp
            sender = history.sender
            content = history.content
            sql = """insert into chat_history values (0,"%s","%s","%s","%s")""" %(group_num,time,sender,content)
            self.cursor.execute(sql)
            self.conn.commit()

    # 添加新用户
    # new_user: User Object
    def add_user(self, new_user):
        self.user_list.append(new_user)
        self.save_user()

    # 移除用户
    # username: str
    # 逻辑删除
    def remove_user(self, username):
        sql = """update userchat set is_delete=1 where username = ("%s")""" %username
        self.cursor.execute(sql)
        self.conn.commit()

    # 通过username查找用户对象
    # username: str
    # return User Object
    def get_user_with_username(self,username):
        sql = """select * from userchat where username = ("%s")""" % username
        self.cursor.execute(sql)
        temp = self.cursor.fetchone()
        print(temp)
        return temp

    # 添加新的聊天群组
    # new_group: Group Object
    def add_group(self, new_group):
        self.group_list.append(new_group)
        self.save_group()

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
        sql = """select * from contacts_chat where group_num = ("%s")""" % group_num
        self.cursor.execute(sql)
        temp = self.cursor.fetchone()
        print(temp)
        return temp


    #添加新的历史记录
    #new_history:HistoryMeta Object
    def add_history(self,new_history):
        self.history_list.append(new_history)
        self.save_history()

    #通过group_num查找历史记录
    def get_history_with_group_num(self,group_num):
        sql = """select * from chat_history where group_num = ("%s")""" % group_num
        self.cursor.execute(sql)
        temp = self.cursor.fetchone()
        print(temp)
        return temp


# 用户
class User:
    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.avatar = kwargs['avatar']
        self.contacts = kwargs['contacts']  # 联系人列表，每个元素为一个Group对象
        self.invitations = kwargs['invitations']  # 邀请列表
        self.email = kwargs['email']
        self.confirmed = kwargs['confirmed']    # 邮箱验证通过标记
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
    # chat_history应该读取数据文件进行初始化
    def __init__(self, members, group_num, group_name):
        self.members = members
        self.group_num = group_num
        self.group_name = group_name
        self.chat_history = ChatHistory(self.group_num)

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
        new_history = HistoryMeta(sender, content)
        self.history.append(new_history)


# 聊天记录元，每个对象包含一条历史消息
class HistoryMeta:
    # 构造函数
    # sender: 发信人用户名 str
    # content: 消息原文 str
    def __init__(self, group_num,sender, content):
        self.group_num = group_num
        self.timestamp = int(time.mktime(time.localtime(time.time())))
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
