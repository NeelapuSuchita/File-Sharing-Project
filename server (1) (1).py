# server.py - Complete implementation (Day 1 to Day 5)
import socket
import os

# --- Authentication Configuration (Day 5) ---
VALID_USERS = {
    "user1": "pass123",
    "admin": "securepwd"
}

# --- Network Configuration (Day 1) ---
HOST = '127.0.0.1'
PORT = 9000
SERVER_DIR = 'SERVER_FILES'

# Ensure the shared directory exists
os.makedirs(SERVER_DIR, exist_ok=True)
print(f"Server will share files from: {SERVER_DIR}")


def handle_client(conn, addr):
    """
    Handles commands (LIST, DOWNLOAD, UPLOAD, LOGIN) from a client connection.
    Requires successful login before file operations are permitted (Day 5).
    """
    print(f"Connected by {addr}")
    conn.sendall(b"HELLO FROM SERVER. PLEASE LOGIN.\n")
    
    # --- Day 5: Initialize Session State ---
    logged_in = False
    
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected.")
                break
            
            command = data.decode().strip()
            print(f"Received command: '{command}'")

            # --- Day 5: Handle LOGIN Command FIRST ---
            if command.startswith("LOGIN"):
                parts = command.split()
                if len(parts) == 3:
                    username = parts[1]
                    password = parts[2]
                    
                    if username in VALID_USERS and VALID_USERS[username] == password:
                        logged_in = True
                        conn.sendall(b"LOGIN_SUCCESS")
                        print(f"User {username} successfully logged in.")
                    else:
                        conn.sendall(b"LOGIN_FAIL: Invalid credentials.")
                        print(f"Login attempt failed for user: {username}")
                else:
                    conn.sendall(b"ERROR: Usage: LOGIN <user> <pass>")
            
            # --- Enforce Authentication for all File Commands ---
            elif logged_in:
                
                # --- Day 2: Implement LIST command ---
                if command == "LIST":
                    file_list = [f for f in os.listdir(SERVER_DIR) if os.path.isfile(os.path.join(SERVER_DIR, f))]
                    list_response = "\n".join(file_list)
                    if not file_list: 
                        list_response = "No files found in SERVER_FILES."
                    
                    conn.sendall(list_response.encode())
                    print("Sent file list to client.")

                # --- Day 3: Implement DOWNLOAD command ---
                elif command.startswith("DOWNLOAD"):
                    parts = command.split(maxsplit=1)
                    if len(parts) < 2:
                        conn.sendall(b"ERROR: Missing filename".encode())
                        continue

                    filename = parts[1]
                    filepath = os.path.join(SERVER_DIR, filename)

                    try:
                        # 1. Get file size and send the size as a 10-byte header
                        filesize = os.path.getsize(filepath)
                        size_header = str(filesize).zfill(10).encode() 
                        conn.sendall(size_header)
                        
                        # 2. Send the file content in chunks
                        with open(filepath, 'rb') as f:
                            while True:
                                bytes_read = f.read(1024)
                                if not bytes_read:
                                    break # File transmission is done
                                conn.sendall(bytes_read)

                        print(f"Sent {filename} ({filesize} bytes) to client.")
                    except FileNotFoundError:
                        # Signal file not found by sending a size of 0
                        conn.sendall(b"0000000000") 
                        print(f"Error: File '{filename}' not found.")
                
                # --- Day 4: Implement UPLOAD command ---
                elif command.startswith("UPLOAD"):
                    parts = command.split(maxsplit=1)
                    if len(parts) < 2:
                        conn.sendall(b"ERROR: Missing upload filename".encode())
                        continue
                    
                    filename = parts[1]
                    filepath = os.path.join(SERVER_DIR, filename)
                    
                    # Send ACK to client to proceed with size and data transfer
                    conn.sendall(b"READY_FOR_UPLOAD")
                    
                    # Receive the file size header (10 bytes)
                    size_header = conn.recv(10).decode()
                    filesize = int(size_header)
                    
                    if filesize == 0:
                        print(f"Error: Client tried to upload empty/non-existent file: {filename}")
                        conn.sendall(b"UPLOAD_FAIL")
                        continue

                    # Receive file content in chunks
                    received_bytes = 0
                    print(f"Receiving {filename} ({filesize} bytes) from client...")
                    
                    with open(filepath, 'wb') as f:
                        while received_bytes < filesize:
                            remaining = filesize - received_bytes
                            bytes_to_read = min(1024, remaining)
                            bytes_read = conn.recv(bytes_to_read)
                            
                            if not bytes_read:
                                break
                                
                            f.write(bytes_read)
                            received_bytes += len(bytes_read)

                    if received_bytes == filesize:
                        print(f"Upload complete: {filename} saved on server.")
                        conn.sendall(b"UPLOAD_SUCCESS")
                    else:
                        print(f"Upload FAILED: Only received {received_bytes}/{filesize} bytes.")
                        conn.sendall(b"UPLOAD_FAIL")

                else:
                    conn.sendall(b"Unknown command.")
            
            # --- Response if Not Logged In ---
            else:
                conn.sendall(b"ERROR: Please log in first using LOGIN <user> <pass>")

        except Exception as e:
            print(f"An error occurred with client {addr}: {e}")
            break
            
    conn.close()


# Server listening setup (Day 1)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Listening on {HOST}:{PORT} ...")
    
    # Simple single-threaded server loop
    while True:
        conn, addr = s.accept()
        handle_client(conn, addr)
