from os import name
import socket
import pickle
import threading
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

def main(name):
    client.connect(ADDR)
    thread1 = threading.Thread(target=send_msg, args=(name,))
    thread1.start()
    thread2 = threading.Thread(target=recv_msg, args=())
    thread2.start()

def send_msg(name):
    connected = True
    while connected:
        NAME = input("")
        msg = name + ":" + NAME
        client.send(bytes(msg, encoding="utf-8"))

def recv_msg():
    connected = True
    while connected:
        message = client.recv(1024).decode("utf-8")
        print(message)

name = input("your name:")
main(name)









