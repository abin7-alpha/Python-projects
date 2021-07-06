"""Imports socket and threading to create socket and thread"""
import socket
import threading

class CLIENT:
    """Creates client connection join it with the server
    and handles the recieve and send purposes"""
    def __init__(self):
        port = 63219
        ip_addr = socket.gethostbyname(socket.gethostname())
        self.addr = (ip_addr, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def join_connection(self, name, room_no, room_name):
        """connect to the server and creates each thread for each
        purposes ie.send/recieve"""
        self.client.connect(self.addr)
        self.client.sendall(str.encode("\n".join([str(room_no), str(room_name), str(name)])))
        thread1 = threading.Thread(target=self.send_msg, args=(name,))
        thread1.start()
        thread2 = threading.Thread(target=self.recv_msg, args=())
        thread2.start()

    def send_msg(self, name):
        """Sends message to the server"""
        connected = True
        while connected:
            message = input("")
            if message == "!exit":
                self.client.send(bytes((f"[{name}] has left the room"),
                                        encoding="utf-8"))
                self.client.close()
            else:
                msg = name + ":" + message
                self.client.send(bytes(msg, encoding="utf-8"))

    def recv_msg(self):
        """Recieve message from the server"""
        connected = True
        while connected:
            message = self.client.recv(1024).decode("utf-8")
            print(message)

    def room_requirements(self):
        """getting the values for chat room"""
        user_name = input("Enter your name:")
        room_no = input("Room_no:")
        room_name = input("Room_name:")
        self.join_connection(user_name, room_no, room_name)

member = CLIENT()
print("[1.Create room][2.Join room]]")
print("[Choose wisely]")
value = input("Your option:")
values = ["1","2"]
if value in values:
    if value == "1":
        member.room_requirements()
    elif value == "2":
        member.room_requirements()
else:
    print("Invalid option")
