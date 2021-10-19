import socket
import message
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#从客户端发送给服务端
def client_to_conn():
	label = get_message_type()
	number = get_number()
	msg = get_raw_message()
	if flag == 0:
		msg = txt_msg(get_raw_message())
	if label == 'group':
		payload = "GET /send_group_msg?group_id=" + str(number) + "&message=" + msg + " HTTP/1.1\r\nHost: 127.0.0.1:5700\r\nConnection: close\r\n\r\n"
	elif label == 'private':
		payload = "GET /send_private_msg?user_id=" + str(number) + "&message=××××" + " HTTP/1.1\r\nHost: 127.0.0.1:5700\r\nConnection: close\r\n\r\n"
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(('127.0.0.1',5700))
	client.send(payload.encode("utf-8"))
	client.close()
while True:
    client_to_conn()
