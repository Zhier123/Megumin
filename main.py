from receive import rev_msg
from send_message.send_message import send_message
from massage_flide import msg_talker

talker = msg_talker()
print("start")
while True:
    try:
        rev = rev_msg()
        if rev == None:
            continue    
    except:
        continue
    if rev["post_type"] == "message":
        print(" ")
        if(rev['sender']['user_id']==792971844 and rev['message']=='Drain'):
            print("program_end")#这是一个终结指令 如果来自我的主号发送了Drain 则关闭程序并向主号回报
            send_message("off\nline",792971844,"private")
            #send_message("offline",657668007,"group")
            break

        #在main.py 中打印 接受到 的所有消息   
        if(rev['group_id']):
            print('from'+format(str(rev['group_id'])))
        print(rev['sender']['nickname']+': '+rev['message']) #需要功能自己DIY
        if rev["message_type"] == "private": #私聊
            talker.private_msg(rev)
        elif rev["message_type"] == "group": #群聊
            talker.group_msg(rev)
        else:
            continue
    elif rev["post_type"] == "notice":
        if rev["notice_type"] == "group_upload":  # 有人上传群文件
            continue
        elif rev["notice_type"] == "group_decrease":  # 群成员减少
            continue
        elif rev["notice_type"] == "group_increase":  # 群成员增加
            continue
        else:
            continue
    elif rev["post_type"] == "request":
        if rev["request_type"] == "friend":  # 添加好友请求
            pass
        if rev["request_type"] == "group":  # 加群请求
            pass
    else:  # rev["post_type"]=="meta_event":
        continue
