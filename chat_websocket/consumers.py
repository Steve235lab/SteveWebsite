# consumers.py
# 实现WebSocket业务逻辑
# Written on 2022/4/2 by Steve D. J.
# Based on the video course
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import time
from .email_sender import EmailSender
from .database import DATABASE, User, Group, HistoryMeta
import re


# 聊天室
class ChatConsumer(WebsocketConsumer):
    chatting_to = None
    user_signed_in = ''

    def websocket_connect(self, message):
        # 接收客户端发送的websocket连接请求，与客户端握手创建连接
        self.accept()
        # 获取username
        username = self.scope['url_route']['kwargs'].get("username")
        self.user_signed_in = username
        # group_add(组号, 为新连接用户生成的组内代号)
        # async_to_sync(self.channel_layer.group_add)(group_num, self.channel_name)
        # 向客户端发送用户名以及联系人列表
        self.send("username=" + username)
        self.send_contacts(username)
        print("已向客户端发送 " + username + ' 的联系人列表')
        # print(self.chatting_to)
        if self.chatting_to != 'None' and self.chatting_to is not None:
            self.send_chat_history()
            print("已向客户端发送 " + str(self.chatting_to) + ' 的聊天记录')

    # 向前端发送联系人列表（实际上是以/分割的字符串）
    def send_contacts(self, username):
        # 调用get_user_index方法，不安全，已废弃
        # user_index = DATABASE.get_user_index(username)
        # if user_index != -1:
        #     contacts = DATABASE.user_list[user_index].contacts
        # else:
        #     contacts = []
        # if len(contacts) == 0:
        #     contacts_str = 'None'
        # else:
        #     contacts_str = ''
        #     for contact in contacts:
        #         group_num = contact.group_num
        #         group_name = contact.group_name
        #         index = group_name.find('、')
        #         if index != -1:
        #             members = group_name.split('、')
        #             for member in members:
        #                 if member != username:
        #                     group_name = member
        #         contacts_str += str(group_num) + ',' + group_name + '/'
        #     contacts_str += 'None'
        # self.send("contacts=" + contacts_str)
        user = DATABASE.get_user_with_username(username)
        if user.username != 'Void':
            contacts = user.contacts
        else:
            contacts = []
        # print(contacts)
        if len(contacts) == 0 or contacts[0] == 'None':
            contacts_str = 'None'
            self.chatting_to = None
        else:
            self.chatting_to = contacts[0]
            contacts_str = ''
            for contact in contacts:
                group_num = contact
                group = DATABASE.get_group_with_group_num(group_num)
                group_name = group.group_name
                # print(group_name)
                group_avatar = group.group_avatar
                group_avatar = group_avatar.split('/')[-1]
                index = group_name.find('、')
                if index != -1:
                    members = group_name.split('、')
                    for member in members:
                        if member != username:
                            group_name = member
                            group_avatar = DATABASE.get_user_with_username(group_name).avatar.split('/')[-1]
                contacts_str += str(group_num) + ',' + group_name + ',' + group_avatar + '/'
            contacts_str += 'None'
        self.send("contacts=" + contacts_str)

    # 发送当前组的聊天记录
    def send_chat_history(self):
        chatting_to = str(self.chatting_to)
        async_to_sync(self.channel_layer.group_add)(chatting_to, self.channel_name)
        chat_history = DATABASE.history_dict[int(self.chatting_to)]
        chat_history_str = 'chat_history='
        if len(chat_history.history) > 0:
            for meta in chat_history.history:
                meta_str = meta.format_str()
                sender = meta.sender
                sender_avatar = DATABASE.get_user_with_username(sender).avatar
                sender_avatar = sender_avatar.split('/')[-1]
                chat_history_str += meta_str + ',' + sender_avatar + '/'
        chat_history_str += 'None'
        self.send(chat_history_str)

    def websocket_receive(self, message):
        # 浏览器基于websocket向后端发送数据，自动触发接收消息，并进行回复
        # message: {'type': 'websocket.receive', 'text': '用户发送的内容'}
        text = message['text']
        print(text)
        # 响应"chatting_to="类型的消息，切换当前聊天群组
        if text[:12] == 'chatting_to=':
            self.chatting_to = int(text[12:])
            self.send_chat_history()
            print("已向客户端发送 " + str(self.chatting_to) + ' 的聊天记录')
        # 响应"new_message="类型的消息，保存新消息并广播
        elif text[:12] == 'new_message=':
            chatting_to = str(self.chatting_to)
            new_meta = HistoryMeta(int(self.chatting_to), self.user_signed_in, text[12:])
            DATABASE.add_history(new_meta)
            async_to_sync(self.channel_layer.group_send)(chatting_to, {"type": "xx.oo", "message": new_meta})
            # DATABASE.save_history(DATABASE.history_dict[self.chatting_to].history[-1])

    def xx_oo(self, event):
        broadcast = 'chat_history='
        meta = event['message']
        timestamp = meta.timestamp
        sender = meta.sender
        content = meta.content
        avatar = DATABASE.get_user_with_username(sender).avatar
        avatar = avatar.split('/')[-1]
        broadcast += str(timestamp) + ',' + sender + ',' + content + ',' + avatar + '/None'
        self.send(broadcast)

    def websocket_disconnect(self, message):
        print("与客户端断开连接")
        username = self.scope['url_route']['kwargs'].get("username")
        # 将用户从组中移除
        # async_to_sync(self.channel_layer.group_discard)(group_num, self.channel_name)
        raise StopConsumer()


# 注册
class SignUpConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 接收客户端发送的websocket连接请求，与客户端握手创建连接
        self.accept()
        print("Sign Up Connected")

    def websocket_receive(self, message):
        text = message['text']
        # 消息解包
        words = text.split('/')
        username = words[0]
        password = words[1]
        email = words[2]
        print("用户：" + username + "正在注册...")
        # 检查用户名与电子邮件地址的合法性
        if self.check_username(username) == 0:
            print("用户名" + username + "已通过检查")
            if self.check_email(email) == 0:
                print("用户邮箱" + email + "已通过检查")
                self.send("OK")
                # 构造新用户对象
                user = User(username=username, password=password, avatar='../static/avatars/Judy.JPG', contacts=[],
                            invitations=[], email=email, confirmed='no', confirm_code='None')
                # 将新用户保存到数据库
                DATABASE.add_user(user)
                # 发送验证邮件
                sender = EmailSender(receiver_address=email, username=username)
                sender.generate_content()
                sender.send()
                self.close()
                print("Sign Up Disconnected")
            else:
                print("用户邮箱" + email + "不合法")
        else:
            print("用户名" + username + "不合法")

    def websocket_disconnect(self, message):
        print("Sign Up Disconnected")
        raise StopConsumer()

    # 检查新用户的用户名是否合法
    def check_username(self, username):
        # 用户名含有特殊符号
        if username.find(':') != -1 or username.find('/') != -1 or username.find('.') != -1 or username.find(',') != -1:
            self.send('invalid username')
            return -1
        else:
            # 生成已注册用户名列表
            username_list = []
            for user in DATABASE.user_list:
                username_list.append(user.username)
            # 用户名已占用
            if username in username_list:
                self.send('username occupied')
                return 1
            # 用户名验证通过
            else:
                return 0

    # 检查用户填写的邮箱是否合法
    def check_email(self, email):
        # 使用通用邮件验证正则表达式 来源：知乎
        # 千万不要碰这个正则表达式
        regex = re.compile(
            r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''')
        # 有效的email地址
        if re.fullmatch(regex, email):
            return 0
        # 无效的email地址
        else:
            self.send('invalid email')
            return -1


# 登录
class SignInConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 接收客户端发送的websocket连接请求，与客户端握手创建连接
        self.accept()
        print("Sign In Connected")

    def websocket_receive(self, message):
        text = message['text']
        # 消息解包
        words = text.split('/')
        username = words[0]
        password = words[1]
        print("用户" + username + "正在登录...")
        # 匹配数据库中已注册用户的密码
        db_password = DATABASE.get_user_password(username)
        # 用户未注册
        if db_password == 'User not registered!':
            self.send("unregistered user")
            print("用户" + username + "未注册")
        # 密码正确
        elif db_password == password:
            self.send("OK")
            print("用户" + username + "登陆成功")
            self.close()
            print("Sign In Disconnected")
        # 密码错误
        else:
            self.send("wrong password")
            print("用户" + username + "密码错误")

    def websocket_disconnect(self, message):
        print("Sign In Disconnected")
        raise StopConsumer()


# 验证邮件
class CfmEmlConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 接收客户端发送的websocket连接请求，与客户端握手创建连接
        self.accept()
        print("Confirm Email Connected")

    def websocket_receive(self, message):
        confirm_code = message['text']
        # print("用户输入的验证码为：" + confirm_code)
        # 通过路由获取正在进行邮件验证的用户名
        username = self.scope['url_route']['kwargs'].get("username")
        print("用户" + username + "正在进行邮箱验证...")
        db_confirm_code = DATABASE.get_confirm_code(username)
        # print("数据库中保存的验证码为：" + db_confirm_code)
        if confirm_code == db_confirm_code:
            # 对用户的confirmed成员进行更改
            user_index = DATABASE.get_user_index(username)
            DATABASE.user_list[user_index].confirmed = 'yes'
            DATABASE.rewrite_user(DATABASE.user_list[user_index])
            print("用户" + username + "邮箱验证成功")
            self.send("email confirmed")
            self.close()
            print("Confirm Email Disconnected")
        else:
            print("用户" + username + "邮箱验证码错误")
            self.send("wrong confirm code")

    def websocket_disconnect(self, message):
        print("Confirm Email Disconnected")
        raise StopConsumer()


# 添加联系人
class AddContactConsumer(WebsocketConsumer):
    user_signed_in = ''

    def websocket_connect(self, message):
        # 接收客户端发送的websocket连接请求，与客户端握手创建连接
        self.accept()
        self.user_signed_in = self.scope['url_route']['kwargs'].get("username")
        print("Add Contact Connected")

    def websocket_receive(self, message):
        username = self.user_signed_in
        text = message['text']
        print(text)
        cmd_key = text.split('=')[0]
        if cmd_key == 'search':     # 处理"search=..."消息
            user_input = text.split('=')[-1]
            try:    # 用户使用组号精确搜索
                group_num = int(user_input)
                matched_group = DATABASE.get_group_with_group_num(group_num)
                if matched_group.group_num != -1:   # 找到组
                    group_name = matched_group.group_name
                    if group_name.find('、') == -1:  # 非私聊组
                        group_avatar = matched_group.group_avatar.split('/')[-1]
                        matched_groups_str = 'matched_groups=' + user_input + ',' + group_name + ',' + group_avatar + '/None'
                        self.send(matched_groups_str)
                        self.send_matched_user(user_input)
                        return None
                    else:   # 私聊组
                        matched_groups_str = 'matched_groups=None'
                        self.send(matched_groups_str)
                        self.send_matched_user(user_input)
                        return None
                else:   # 未通过组号找到组
                    self.send_matched_user(user_input)
                    self.send_name_matched_group(user_input)
                    return None
            except:     # 用户使用用户名或组名进行搜索
                self.send_matched_user(user_input)
                self.send_name_matched_group(user_input)
                return None
        if cmd_key == 'add_friend':     # 当前登录的用户添加另一名用户为好友
            friend_name = text.split('=')[-1]
            if len(DATABASE.group_list) > 0:
                new_group_num = int(DATABASE.group_list[-1].group_num) + 1
            else:
                new_group_num = 0
            group_name = username + '、' + friend_name
            group_name2 = friend_name + '、' + username
            if self.search_name_matched_group(group_name) == 0 and self.search_name_matched_group(group_name2) == 0:
                new_group = Group([username, friend_name], new_group_num, group_name)
                DATABASE.add_group(new_group)
                host = DATABASE.get_user_with_username(username)
                host.contacts.append(new_group_num)
                host_index = DATABASE.get_user_index(username)
                DATABASE.user_list[host_index] = host
                DATABASE.rewrite_user(host)
                friend = DATABASE.get_user_with_username(friend_name)
                friend.contacts.append(new_group_num)
                friend_index = DATABASE.get_user_index(friend_name)
                DATABASE.user_list[friend_index] = friend
                DATABASE.rewrite_user(friend)
                print("add friend success")
            else:
                print("不可重复添加好友")
        if cmd_key == 'add_group':      # 当前登录的用户加入一个已经存在的群聊
            try:
                group_num = int(text.split('=')[-1])
                group = DATABASE.get_group_with_group_num(group_num)
                print("host = ", username)
                group.add_member(username)
                DATABASE.rewrite_group(group)
                host = DATABASE.get_user_with_username(username)
                host.contacts.append(group_num)
                host_index = DATABASE.get_user_index(username)
                DATABASE.user_list[host_index] = host
                DATABASE.rewrite_user(host)
            except:
                pass
        if cmd_key == 'new_group':      # 当前登录的用户创建一个新的群聊
            group_name = text.split('=')[-1]
            if len(DATABASE.group_list) > 0:
                new_group_num = int(DATABASE.group_list[-1].group_num) + 1
            else:
                new_group_num = 0
            new_group = Group([username], new_group_num, group_name)
            DATABASE.add_group(new_group)
            user = DATABASE.get_user_with_username(username)
            user.contacts.append(new_group_num)
            user_index = DATABASE.get_user_index(username)
            DATABASE.user_list[user_index] = user
            DATABASE.rewrite_user(user)

    def send_matched_user(self, username):
        matched_user = DATABASE.get_user_with_username(username)
        if matched_user.username != 'Void':
            matched_user_str = 'matched_users=' + username + ','
            matched_user_str += matched_user.avatar.split('/')[-1] + '/None'
        else:
            matched_user_str = 'matched_users=None'
        self.send(matched_user_str)

    def send_name_matched_group(self, group_name):
        if group_name.find('、') == -1:      # 非私聊组
            print("正在使用组名查找非私聊组")
            matched_groups_str = 'matched_groups='
            for group in DATABASE.group_list:
                if group_name == group.group_name:
                    print("使用组名查找成功")
                    matched_groups_str += str(group.group_num) + ','
                    matched_groups_str += group_name + ','
                    matched_groups_str += group.group_avatar.split('/')[-1] + '/'
                    break
            matched_groups_str += 'None'
        else:   # 私聊组返回未找到
            matched_groups_str = 'matched_groups=None'
        self.send(matched_groups_str)
        print("已发送：", matched_groups_str)

    def search_name_matched_group(self, group_name):
        matched_flag = 0
        for group in DATABASE.group_list:
            if group_name == group.group_name:
                matched_flag = 1
                break

        return matched_flag


