import socket
import threading
import json

PORT = 63219

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

MY_CLIENTS = {}

CHAT_ROOMS = {}

MESSAGES = {}

def main():
    global MY_CLIENTS
    global CHAT_ROOMS
    server.listen(10)
    print("Server is listening")
    while True:
        conn, addr = server.accept()
        room_no, room_name, user_name= [str(i) for i in conn.recv(1024).decode('utf-8').split("\n")]
        if room_no not in MY_CLIENTS:
            MY_CLIENTS[room_no] = [conn]
        else:
            MY_CLIENTS[room_no].append(conn)
        CHAT_ROOMS[room_no] = room_name
        thread = threading.Thread(target=handle_clients, args=(conn, room_name, room_no, user_name))
        thread.start()

def handle_clients(conn, room_name, room_no, user_name):
    global MESSAGES
    quit = "!exit"
    print(f"{user_name} joined in {room_name} with {room_no}.")
    connected = True
    while connected:
        msg  = conn.recv(1024).decode("utf-8")
        if msg == quit:
            break
        print(f"[{room_name}]:{msg}")  
        if room_name not in MESSAGES:
            MESSAGES[room_name] = [msg]
        else:
            MESSAGES[room_name].append(msg)    
        if msg:
            thread = threading.Thread(target=client_communication, args=(conn, room_name, room_no))
            thread.start()
    print(f"{user_name}disconnected")        
    conn.close()

def client_communication(conn, room_name, room_no):
    clients = MY_CLIENTS[room_no]
    clients.remove(conn)
    messages = MESSAGES[room_name]
    for client in clients:
        client.send(bytes(messages[-1], encoding="utf-8"))
    clients += [conn]    

main()    