import socket
import threading
import json

Header = 64
NUM_STU = 1
PORT = 4500
DISCONNECT_MSG = "!Disconnected"
STUDENT_INFO="Student information"
SERVER = socket.gethostbyname(socket.gethostname()) #local ipv add

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#socket.AF_INET  >> what type of add acc or loking for
server.bind((SERVER, PORT))

	
def save_student_info(conn, addr): 
	conn.send("Saving student info ....".encode('utf-8'))
	connected = True
	while connected:
		msg_legnth = conn.recv(Header).decode('utf-8')
		if len(msg_legnth):

			msg_legnth = int(msg_legnth)
			msg = conn.recv(msg_legnth).decode('utf-8')
			print(msg)
			connected = False
			with open('json_data'+str(addr)+'.json', 'w') as outfile:
				outfile.write(msg)
			conn.send("informations saved.".encode('utf-8'))
			return json.loads(msg)
def students_avg(informations):
	ave = {}
	for i in range(NUM_STU):

		ave[informations[str(i)]['national code']] = sum(informations[str(i)]['marks']) / 5
		ave = json.dumps(ave)
	conn.send(ave.encode('utf-8'))


def sort_avg(informations):
	sorted_avg = {}
	for i in range(NUM_STU):

		sorted_avg[informations[str(i)]['SSN']] = sum(informations[str(i)]['marks']) / 5
		sorted_avg = sorted(sorted_avg.items(), key = lambda kv: kv[1])
		sorted_avg = json.dumps(sorted_avg)

	conn.send(sorted_avg.encode('utf-8'))
def Max_avg(informations):


def Min_avg(informations):

def handle_client(conn, addr):

	print(f"[NEW CONNECTION ]{addr} connected.")

	connected = True
	informations = {}

	while connected:
		msg_legnth = conn.recv(Header).decode('utf-8')
		
		if len(msg_legnth):

			msg_legnth = int(msg_legnth)
			msg = conn.recv(msg_legnth).decode('utf-8')
			print(f"[{addr}]{msg}")
			if msg == STUDENT_INFO:
				informations = save_student_info(conn, addr)
	
			elif msg == 'Average':

				students_avg(informations)

			elif msg=='Sort':

				sort_avg(informations)

			elif msg=="Max":

				Max_avg(informations)

			elif msg=="Min":
				
				Min_avg(informations)
				
			else:
				connected = False
				conn.send("!Disconnected".encode('utf-8'))
				print(f"[{addr} Connection Closed. ACTIVE CONNECTIONS]  \
				{threading. active_count() - 2}")


			

	conn.close()




def start_server():

	server.listen()
	while True :
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS]   {threading. active_count() - 1}")

print("[SERVER IS STARTING...]")
start_server()
