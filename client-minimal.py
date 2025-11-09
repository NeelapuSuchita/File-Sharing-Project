# client_minimal.py - connect to Day-1 server
import socket

HOST = '127.0.0.1'
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    greeting = s.recv(1024)
    print("Server said:", greeting.decode().strip())
    s.sendall(b"HELLO FROM CLIENT\n")
