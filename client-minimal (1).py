# client_minimal.py - connect to Day-1 server
import socket

HOST = '127.0.0.1'
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    greeting = s.recv(1024)
    print("Server said:", greeting.decode().strip())
    s.sendall(b"HELLO FROM CLIENT\n")
# client.py - Updated for LIST command

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f"Error: Could not connect to server at {HOST}:{PORT}. Ensure server.py is running.")
            return

        # 1. Receive initial greeting from server
        greeting = s.recv(1024).decode().strip()
        print("Server said:", greeting)

        # --- Day 2: Send LIST command ---
        s.sendall(b"LIST") 
        
        # 2. Receive the file list from the server (using a larger buffer)
        file_list_data = s.recv(4096) 
        
        # 3. Decode and print the list
        file_list = file_list_data.decode().strip()
        print("\n--- Files on Server ---")
        print(file_list)
        print("-----------------------")

        # After LIST command, you can add DOWNLOAD logic here (Phase 2)
        # s.sendall(b"DOWNLOAD your_file.txt") 
        # ... receive file content ...

        # Keep the connection open for a bit, or close it after a command
        # For now, the script will exit after executing the LIST command
        
        print("Client closing connection.")


if __name__ == '__main__':
    run_client()
