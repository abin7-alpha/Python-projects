import socket
import json
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 63219
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

def main(name, room_no, room_name):
    client.connect(ADDR)
    client.sendall(str.encode("\n".join([str(room_no), str(room_name), str(name)])))
    thread1 = threading.Thread(target=send_msg, args=(name,))
    thread1.start()
    thread2 = threading.Thread(target=recv_msg, args=())
    thread2.start()

def send_msg(name):
    connected = True
    while connected:
        message = input("")
        if message == "!exit":
            client.send(bytes((f"[{name}] has left the room"), encoding="utf-8"))
            client.close()
        else:
            msg = name + ":" + message
            client.send(bytes(msg, encoding="utf-8"))

def recv_msg():
    connected = True
    while connected:
        message = client.recv(1024).decode("utf-8")
        print(message)

def create_room():
    user_name = input("Enter your name:")
    room_no = input("Room_no:")
    room_name = input("Room_name:")
    main(user_name, room_no, room_name)

def available_rooms():
    client.connect(ADDR)
    rooms_list = client.recv(1024).decode("utf-8")
    data = json.loads(rooms_list)
    print(data)

def join_room():
    user_name = input("Your name:")
    room_no = input("Room_no:")
    room_name = input("Room_name:")
    main(user_name, room_no, room_name)

print("[1.Create Room][2.Join Room]")
print("Choose wisely")
value = input("Your option:")
values = ["1","2"]
if value in values:
    if value == "1":
        create_room()
    elif value == "2":
        join_room()
else:
    print("Invalid option") 
        

    
    











