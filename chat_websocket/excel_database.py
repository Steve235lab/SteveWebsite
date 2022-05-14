# excel_database.py
# 基于excel的简易数据库
# Written on 2022/5/8 by Steve D. J.

import pandas as pd
import time


class ExcelDatabase:
    excel_file_path = 'chat_websocket/database.xlsx'
    user_list = []

    # 读取excel文件初始化对象
    def __init__(self):
        data = pd.read_excel(self.excel_file_path, 'Sheet1', index_col=None, header=0)
        for i in data.index:
            # 读取原始数据
            username = data.iloc[i, 0]
            if username == '':
                break
            password = data.iloc[i, 1]
            avatar = data.iloc[i, 2]
            invitations_str = data.iloc[i, 3]
            email = data.iloc[i, 4]
            confirmed = data.iloc[i, 5]
            confirm_code = data.iloc[i, 6]
            contacts_str = data.iloc[i, 7]
            # 分割为list对象
            invitations = invitations_str.split('/')
            contacts_temp = contacts_str.split('/')
            # 空列表判断
            if invitations[0] == 'None':
                invitations = []
            contacts = []
            if contacts_temp[0] != 'None':
                # 构造Group对象添加至contacts列表中
                for i in range(len(contacts_temp)):
                    cache = contacts_temp[i].split(',')
                    group_num = cache[0]
                    group_name = cache[1]
                    contact = Group(group_num=group_num, group_name=group_name)
                    contacts.append(contact)
            # 构造User对象
            user = User(username=username, password=password, avatar=avatar, contacts=contacts,
                        invitations=invitations, email=email, confirmed=confirmed, confirm_code=confirm_code)
            # 将User对象放入user_list
            self.user_list.append(user)

    # 将新用户添加到用户列表
    # user: User Obj
    def add_user(self, user):
        self.user_list.append(user)
        print("已将用户" + user.username + "添加至用户列表")

    # 将DATABASE对象写入硬盘
    def write_file(self):
        # 将user_list按照协议格式写入文件
        writer = pd.ExcelWriter(self.excel_file_path)
        data_list = []
        for user in self.user_list:
            # 将list对象格式化为字符串
            if len(user.friends) != 0:
                friends_str = user.friends[0]
                for friend in user.friends[1:]:
                    friends_str += '/' + friend
            else:
                friends_str = 'None'
            if len(user.groups) != 0:
                groups_str = user.groups[0]
                for group in user.groups[1:]:
                    groups_str += '/' + group
            else:
                groups_str = 'None'
            if len(user.invitations) != 0:
                invitations_str = user.invitations[0]
                for invitation in user.invitations[1:]:
                    invitations_str += '/' + invitation
            else:
                invitations_str = 'None'
            line = [user.username, user.password, user.avatar, friends_str, groups_str, invitations_str, user.email, user.confirmed, user.confirm_code]
            data_list.append(line)
        data = pd.DataFrame(data_list)
        data.to_excel(writer, sheet_name='Sheet1', index=False,
                      header=['username', 'password', 'avatar', 'friends', 'groups', 'invitations', 'email', 'confirmed', 'confirm_code'])
        writer.save()
        print("数据已保存")

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

    # 将验证码关联到对应的用户
    # username: str
    # confirm_code: str
    def set_confirm_code(self, username, confirm_code):
        for i in range(len(self.user_list)):
            if username == self.user_list[i].username:
                self.user_list[i].confirm_code = confirm_code
                self.write_file()
                # print("已将验证码关联到用户")

    # 通过用户名查找验证码
    # username: str
    def get_confirm_code(self, username):
        for i in range(len(self.user_list)):
            if username == self.user_list[i].username:
                return self.user_list[i].confirm_code

    # 查找指定用户在用户列表中的序号
    # username: str
    # 多用户同时访问时可能存在安全隐患
    def get_user_index(self, username):
        for i in range(len(self.user_list)):
            if username == self.user_list[i].username:
                return i
        # 没找到返回-1
        return -1


class User:
    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.avatar = kwargs['avatar']
        self.invitations = kwargs['invitations']  # 邀请列表
        self.email = kwargs['email']
        self.confirmed = kwargs['confirmed']    # 邮箱验证通过标记
        self.confirm_code = kwargs['confirm_code']  # 发给用户的邮箱验证码
        self.contacts = kwargs['contacts']      # 每一个成员都是一个Group对象


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
    def __init__(self, group_num, group_name):
        # TODO: members成员应该通过读取数据文件初始化
        self.members = []
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


class ChatHistory:
    # 构造函数
    # 读取数据文件初始化对象
    # group_num: int
    # history: list of HistoryMeta objects
    def __init__(self, group_num):
        self.group_num = group_num
        # TODO: 添加读取数据文件初始化聊天记录的功能
        self.history = []

    # 向聊天记录中添加一条新消息
    def add_history(self, sender, content):
        new_history = HistoryMeta(sender, content)
        self.history.append(new_history)


class HistoryMeta:
    # 构造函数
    # sender: 发信人用户名 str
    # content: 消息原文 str
    def __init__(self, sender, content):
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


# 创建全局对象
DATABASE = ExcelDatabase()
