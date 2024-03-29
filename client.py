import socket
import threading
import json

DISCONNECT_MSG = "!Disconnected"
STUDENT_INFO="Student information"
SERVER = "192.168.196.224"
PORT = 4500



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))




def send_msg(msg):
	message = msg.encode('utf-8')
	msg_legnth = len(message)
	send_legnth = str(msg_legnth).encode('utf-8')
	send_legnth += b' ' * (64 - len(send_legnth))
	client.send(send_legnth)
	client.send(message)
	print(client.recv(2048).decode('utf-8'))

def get_student_info():
	information ={}
	print("Please Enter the Student first name:")
	information['name'] = input()
	print("Please Enter the Student last name:")
	information['last_name'] = input()
	print("Please Enter the Student national code:")
	information['national code'] = input()
	print("Please Enter the Student ssn")
	information['SSN'] = input()
	marks = []
	for i in range(5):
		print("Please Enter the Student mark:")
		m = int(input())
		marks.append(m)
	information['marks'] = marks
	return information

def send_students_info():
	print("Enter the number of students:")
	s_num = int(input())
	informations = {}

	for i in range(s_num):
		print("Enter the Student " + str(i)+" information:")
		informations[str(i)] = get_student_info()
	informations = json.dumps(informations)
	send_msg(STUDENT_INFO)
	send_msg(informations)

connected = True
while connected:

	input_string = input()
	if input_string == DISCONNECT_MSG:
		connected = False
		send_msg(DISCONNECT_MSG)
	elif input_string == STUDENT_INFO:
		send_students_info()
	elif input_string == 'Average':
		send_msg('Average')
	elif input_string == 'Sort':
		send_msg('Sort')
	elif input_string == 'Max':
		send_msg('Max')
	elif input_string == 'Min':
		send_msg('Min')
	#send_msg(input_string)
