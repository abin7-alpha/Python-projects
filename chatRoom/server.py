import socket
import pickle
import threading

PORT = 5050

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

MY_CLIENTS = []

MESSAGES = []

MESSAGE_HISTORY = {}

CONNECTED_CLIENTS = []

def main():
    global MY_CLIENTS
    server.listen(10)
    print("Server is listening")
    while True:
        conn, addr = server.accept()
        MY_CLIENTS += [conn]
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()

def handle_clients(conn, addr):
    global MESSAGES
    quit = "!exit"
    print(f"New connections {addr} connected.")
    connected = True
    while connected:
        msg  = conn.recv(1024).decode("utf-8")
        if msg == quit:
            break
        print(f"[{addr}]:{msg}")  
        MESSAGES += [msg]
        if msg:
            thread = threading.Thread(target=client_communication, args=(conn,))
            thread.start()
    print(f"{addr}disconnected")        
    conn.close()

def client_communication(conn):
    clients = MY_CLIENTS
    clients.remove(conn)
    messages = MESSAGES
    for client in clients:
        client.send(bytes(messages[-1], encoding="utf-8"))
    clients += [conn]    

main()        






