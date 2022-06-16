import socket
import threading

Header = 64
PORT = 4500
DISCONNECT_MSG = "!Disconnected"
SERVER = socket.gethostbyname(socket.gethostname()) #local ipv add

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#socket.AF_INET  >> what type of add acc or loking for
server.bind((SERVER, PORT))


def handle_client(conn, addr):

	print(f"[NEW CONNECTION ]{addr} connected.")

	connected = True
	while connected:
		msg_legnth = conn.recv(Header).decode('utf-8')
		if len(msg_legnth):

			msg_legnth = int(msg_legnth)
			msg = conn.recv(msg_legnth).decode('utf-8')
			print(f"[{addr}]{msg}")

			if msg == DISCONNECT_MSG:
				connected = False
				
	conn.close()
	print(f"[{addr} Connection Closed. ACTIVE CONNECTIONS]   {threading. active_count() - 2}")


	


def start_server():

	server.listen()
	while True :
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS]   {threading. active_count() - 1}")

print("SERVER IS STARTING...")
start_server()