import socket
import threading
import json
import os
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
def students_avg(informations, conn):
    ave = {}

    for i in range(len(informations)):
        key = str(informations[str(i)]['national code'])
        ave[key] = sum(informations[str(i)]['marks']) / 5
    ave = json.dumps(ave)
    print(informations)
    conn.send(ave.encode('utf-8'))


def sort_avg(informations, conn):
    sorted_avg = {}
    for i in range(len(informations)):

        sorted_avg[informations[str(i)]['SSN']] = sum(informations[str(i)]['marks']) / 5
    sorted_avg = sorted(sorted_avg.items(), key = lambda kv: kv[1])
    sorted_avg = json.dumps(sorted_avg)

    conn.send(sorted_avg.encode('utf-8'))
def Max_avg(informations, conn):
    sorted_avg = {}
    for i in range(len(informations)):
        sorted_avg[str(i)] = sum(informations[str(i)]['marks']) / 5

    sorted_avg = sorted(sorted_avg.items(), key = lambda kv: kv[1])

    last = str(sorted_avg[len(informations)-1][0])
    print(last)
    print(sorted_avg[len(informations)-1][0])
    result={'name':informations[last]['name'], 'last_name': informations[last]['last_name'], 'avg': sorted_avg[len(informations)-1][1]}
    result = json.dumps(result)
    conn.send(result.encode('utf-8'))


def Min_avg(informations, conn):
    sorted_avg = {}
    for i in range(len(informations)):
        sorted_avg[str(i)] = sum(informations[str(i)]['marks']) / 5

    sorted_avg = sorted(sorted_avg.items(), key = lambda kv: kv[1])
    first = str(sorted_avg[0][0])

    result={'name':informations[first]['name'], 'last_name': informations[first]['last_name'], 'avg': sorted_avg[0][1]}
    result = json.dumps(result)
    conn.send(result.encode('utf-8'))


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

                students_avg(informations, conn)

            elif msg=='Sort':

                sort_avg(informations, conn)

            elif msg=="Max":

                Max_avg(informations, conn)

            elif msg=="Min":
                
                Min_avg(informations, conn)

            else:
                connected = False
                conn.send("!Disconnected".encode('utf-8'))
                print(f"[{addr} Connection Closed. ACTIVE CONNECTIONS]  \
                {threading. active_count() - 2}")


            

    conn.close()




def start_server():

    server.listen()
    dept_num = int(input("Enter number of departments: "))

        
    for i in range(dept_num):
        os.system("start /B start cmd.exe @cmd /c python client.py")
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]   {threading. active_count() - 1}")


print("[SERVER IS STARTING...]")
start_server()