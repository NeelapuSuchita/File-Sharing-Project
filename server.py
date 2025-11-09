# server.py - Minimal Day 1 test server
import socket

HOST = '127.0.0.1'
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Listening on {HOST}:{PORT} ...")
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        conn.sendall(b"HELLO FROM SERVER\n")
        data = conn.recv(1024)
        print("Received from client:", data.decode().strip())
