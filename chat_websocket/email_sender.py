# email_sender.py
# 通过SMTP协议发送电子邮件
# Written on 2022/5/7 by Steve D. J.

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import numpy as np
from .excel_database import DATABASE


class EmailSender:
    auth_passport = 'lwgqxyeerrvtdjgd'
    sender = '2353720063@qq.com'
    subject = 'Steve Website Chatroom sign up confirming email'

    def __init__(self, receiver_address, username):
        self.receivers = []
        self.receivers.append(receiver_address)
        self.username = username
        self.server = smtplib.SMTP()
        self.server.connect('smtp.qq.com')
        self.server.login('2353720063@qq.com', self.auth_passport)
        self.message = None
        self.content = None

    def generate_content(self):
        # 生产随机8位验证码
        confirm_code = ''
        base = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f',
                'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q',
                'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z']
        base_len = len(base)
        for i in range(8):
            base_index = np.random.randint(0, base_len)
            confirm_code += base[base_index]
        # 将验证码关联至用户
        DATABASE.set_confirm_code(self.username, confirm_code)
        cfm_eml_url = 'http://42.192.44.52:8000/websocket/email_confirm/?username=' + self.username
        # 拼接邮件正文内容
        self.content = self.username + '，你好！\n' \
                                       '之所以会收到这封电子邮件是因为你刚刚在Steve的个人网站使用这个邮箱注册了账号。\n' \
                                       '如果你没有进行注册操作，请忽略此邮件。\n' \
                                       '你的验证码为：' + confirm_code + '\n' \
                                       '如果网页没有正常跳转，你可以通过该链接访问邮箱验证页面：' + cfm_eml_url + '\n' \
                                       '该邮件由程序自动生成并发送，请勿回复此邮件。'
        # 设定邮件正文和标题
        self.message = MIMEText(self.content, 'plain', 'utf-8')
        self.message['Subject'] = Header(self.subject, 'utf-8')

    def send(self):
        self.server.sendmail(self.sender, self.receivers, self.message.as_string())
        print("已向用户" + self.username + "的电子邮箱" + self.receivers[0] + "发送验证邮件")
