添加联系人页面websocket会话数据通信协议.md
本协议文件规定了添加联系人页面前端与后端的websocket会话数据通信的格式
Written on 2022/5/20 by Steve D. J.

请保持本协议始终为最新版！

1. 握手成功后不额外发送消息。

2. 用户输入要搜索的用户名/群组名/群组号，点击“搜索”按钮，触发searchContact()函数，向后端发送消息：
    search=search_key_words
    其中search_key_words为用户输入的原始内容。

3. 后端收到"search=..."消息后进行查找，向前端返回查找结果，结果分为两条消息发送：
    匹配的用户 matched_users=username1,user_avatar1/username2,user_avatar2/.../None
            没有找到合适结果时 matched_users=None
    匹配的群组 matched_groups=group_num1,group_name1,group_avatar1/group_num2,group_name2,group_avatar2/.../None
            没有找到合适结果时 matched_groups=None
    目前仅做精确查找功能，即返回的结果一共有以下几种可能：
	· 用户输入组号（数字）精确查找到非私聊群组：matched_users=None  
							matched_groups=group_num1,group_name1,group_avatar1/None
	· 用户输入非数字精确查找到用户： matched_users=username1,user_avatar1/None
							matched_groups=None
	· 用户输入非数字精确查找到群组：matched_users=None  
							matched_groups=group_num1,group_name1,group_avatar1/group_num2,group_name2,group_avatar2/.../None		# 可能存在重名群组
	· 用户输入非数字精确查找到与某个群组重名的用户与群组：matched_users=username1,user_avatar1/None
							matched_groups=group_num1,group_name1,group_avatar1/group_num2,group_name2,group_avatar2/.../None		# 可能存在重名群组
	· 用户输入非数字未查找到结果：matched_users=None   matched_groups=None
			*****此时前端应生成一个按钮用来新建多人组，用户点击此按钮前端向后端发 new_group=search_key_words*****
							
4. 前端接收到后端返回的查找结果后生成列表元素，用户进行选择后，向后端发送选中的结果：
    选择的为用户 add_friend=username
    选择的为群组 add_group=group_num

5. 后端收到选择结果后直接完成关系添加，并断开websocket连接。