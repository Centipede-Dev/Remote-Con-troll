import socket
import time
import sys
HEADER = 64
PORT = 9718
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
serverip4 = input("Enter the IPv4 adress of the target machine: ")
SERVER = serverip4
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


while True:
    prompt = input(f"{SERVER}:/ #  ")
    if prompt == "shutdown":
        print("Closing terminal in 5 seconds...")
        send(prompt)
        time.sleep(5)
        sys.exit()
    else:
        send(prompt)
