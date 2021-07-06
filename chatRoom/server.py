"""Imports socket and threading to create socket and thread"""
import socket
import threading

class SERVER:
    """class server is to create a server and
    handling clients connected in the server"""
    def __init__(self):
        port = 63219
        ip_addr = socket.gethostbyname(socket.gethostname())
        addr = (ip_addr, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.my_clients = {}
        self.chat_rooms = {}
        self.messages = {}

    def start(self):
        """To put the server in to listening mode and recieve messages
        from connected clients,and creates each thread for each client"""
        self.server.listen(10)
        print("Server is listening")
        while True:
            conn, addr = self.server.accept()
            room_no, room_name, user_name = [str(i)
                                             for i in conn.recv(1024)
                                             .decode('utf-8').split("\n")]
            print(f"{user_name} joined in {room_name} with this {addr}.")
            if room_no not in self.my_clients:
                self.my_clients[room_no] = [conn]
            else:
                self.my_clients[room_no].append(conn)
            self.chat_rooms[room_no] = room_name
            thread = threading.Thread(target=self.handle_clients,
                                      args=(conn, room_name, room_no, user_name))
            thread.start()

    def handle_clients(self, conn, room_name, room_no, user_name):
        """Handle the clients that coming with messages and creates
        each purpose-thread for each client"""
        quit_message = "!exit"
        connected = True
        while connected:
            msg  = conn.recv(1024).decode("utf-8")
            if msg == quit_message:
                break
            print(f"[{room_name}]:{msg}")
            if room_name not in self.messages:
                self.messages[room_name] = [msg]
            else:
                self.messages[room_name].append(msg)
            if msg:
                thread = threading.Thread(target=self.client_communication,
                                          args=(conn, room_name, room_no))
                thread.start()
        print(f"{user_name}disconnected")
        conn.close()

    def client_communication(self, conn, room_name, room_no):
        """Handles the client to client commucication without leaking
        messages to another room"""
        clients = self.my_clients[room_no]
        clients.remove(conn)
        messages = self.messages[room_name]
        for client in clients:
            client.send(bytes(messages[-1], encoding="utf-8"))
        clients += [conn]

run_server = SERVER()
run_server.start()
