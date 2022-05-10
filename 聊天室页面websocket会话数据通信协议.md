聊天室页面websocket会话数据通信协议.md
本协议文件规定了聊天室页面前端与后端的websocket会话数据通信的格式
Written on 2022/5/10 by Steve D. J.

请保持本协议始终为最新版！

1. 用户登录成功，前端与后端建立websocket会话
   (1) 后端在websocket_connect()中获取链接中的username，并以"username=xxx"的格式发送至前端。
        消息样例：username=Steve
   (2) 使用username在数据库中查找对应用户的联系人列表（好友列表和群组列表），将联系人列表拼接成字符串后发送至前端。
       具体拼接方式为：group_num1,group_name1/group_num2,group_name2/...
       当联系人列表为空时，会发送None，参考消息样例第二条。
       消息样例：contacts=001,野兽先辈/002,网络程序设计项目组
                contacts=None
    (3) 进入聊天室页面，自动选中contacts列表中的第一个作为“当前聊天对象”。
        无需后端发送额外消息，前端接收到contacts完成界面初始化后默认选中contacts列表中的第一个作为“当前聊天对象”。
        后端默认选中contacts列表中的第一个作为“当前聊天对象”，并向前端发送"当前聊天对象"的chat_history。
        chat_history数据格式：(暂定使用字符串，研究一下使用json对象的必要性以及可行性)
            chat_history=timestamp,sender,content/.../...
            即每条历史消息由时间戳timestamp + 发信者用户名sender + 消息内容content组成，三部分之间使用逗号分隔；消息与消息之间使用/分隔。
            如果消息中含有'/'，则服务器发送时使用该条消息的时间戳代替'/'。
            消息样例：chat_history=1652119534,Steve,Hello world!/1652119569,野兽先辈,test 1652119569

2. 会话建立后
    (1) 前端用户点击按钮选择“当前聊天对象”。
        前端向后端发送 chatting_to=group_num
        消息样例：chatting_to=001
        后端收到chatting_to消息后更改"当前聊天对象"，并向前端发送"当前聊天对象"的chat_history。
        chat_history数据格式见上。
    (2) 用户发送消息。
        前端向后端发送 new_message=xxx
        消息样例：new_message=你好，我发送了一条新消息。
    (3) 服务器接收到new_message，获取当前时间戳，将其打包添加至chat_history，然后：
        ***使用async_to_sync(self.channel_layer.group_send)(group_num, {"type": "xx.oo", "message": new_message})广播方法将该消息进行广播***
        其中xx_oo()方法向前端广播的消息格式为：
            new_msg_broadcast=timestamp,sender,content

3. websocket会话断开
    前端关闭网页自动断开，后端不会主动执行断开命令。

    