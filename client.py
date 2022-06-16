import socket
import threading
DISCONNECT_MSG = "!Disconnected"
SERVER = "192.168.1.6"
PORT = 4500
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((SERVER, PORT))

def send_msg(msg):
	message = msg.encode('utf-8')
	msg_legnth = len(message)
	send_legnth = str(msg_legnth).encode('utf-8')
	send_legnth += b' ' * (64 - len(send_legnth))
	client.send(send_legnth)
	client.send(message )
	print(client.recv(2048).decode('utf-8'))

connected = True
while connected:

	input_string = input()
	if input_string == DISCONNECT_MSG:
		connected = False
	send_msg(input_string)
