# server.py - Updated for LIST and initial command handling
import socket
import os  # <-- Step 1: Import os module

HOST = '127.0.0.1'
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Listening on", HOST, PORT)
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        conn.sendall(b"HELLO\n")
        data = conn.recv(1024)
        print("Received:", data)


SERVER_DIR = 'SERVER_FILES'  # <-- Step 2: Define shared directory

# Ensure the shared directory exists
os.makedirs(SERVER_DIR, exist_ok=True)
print(f"Server will share files from: {SERVER_DIR}")

def handle_client(conn, addr):
    """Handles commands from a single client connection."""
    print(f"Connected by {addr}")
    conn.sendall(b"HELLO FROM SERVER\n")

    # Main command loop: Server listens for commands until client disconnects
    while True:
        try:
            # Receive up to 1024 bytes (e.g., "LIST" or "DOWNLOAD file.txt")
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected.")
                break
            
            command = data.decode().strip()
            print(f"Received command: '{command}'")

            # --- Day 2: Implement LIST command ---
            if command == "LIST":
                # 1. Get the list of files in the shared directory
                file_list = [f for f in os.listdir(SERVER_DIR) if os.path.isfile(os.path.join(SERVER_DIR, f))]
                
                # 2. Format the list into a single string
                list_response = "\n".join(file_list)
                
                if not file_list:
                     list_response = "No files found in SERVER_FILES."

                # 3. Send the list back to the client
                conn.sendall(list_response.encode())
                print("Sent file list to client.")
            
            elif command.startswith("DOWNLOAD"):
                # Day 3 logic will go here
                conn.sendall(b"COMMAND_DOWNLOAD_RECEIVED") # Placeholder response

            else:
                conn.sendall(b"Unknown command.")

        except Exception as e:
            print(f"An error occurred with client {addr}: {e}")
            break
            
    conn.close()


# Server listening setup
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5) # Listen for up to 5 connections
    print(f"Listening on {HOST}:{PORT} ...")
    
    # Simple single-threaded server (replace with threading for multiple clients later)
    while True:
        conn, addr = s.accept()
        # Use conn inside a function or a thread for better structure
        handle_client(conn, addr)

        # --- Current structure inside handle_client(conn, addr): ---
    while True:
        try:
            # ... (receive command logic) ...
            command = data.decode().strip()

            # --- Day 2: Implement LIST command ---
            if command == "LIST":
                # ... (LIST logic) ...
            
            # --- Day 3: Implement DOWNLOAD command ---
            elif command.startswith("DOWNLOAD"):
                # ... (DOWNLOAD logic) ...
            
            # 📢 INSERT THE DAY 4 UPLOAD LOGIC HERE 📢
            # --- Day 4: Implement UPLOAD command (Client to Server) ---
            elif command.startswith("UPLOAD"):
                # COPY AND PASTE THE CODE BLOCK BELOW HERE
                # ...
            
            else:
                conn.sendall(b"Unknown command.")

        except Exception as e:
# ... (rest of function) ...

# ... (after the elif command.startswith("DOWNLOAD"): block) ...
            
            # --- Day 4: Implement UPLOAD command (Client to Server) ---
            elif command.startswith("UPLOAD"):
                # 1. Parse filename and receive the 10-byte size header
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
                    continue

                # 2. Receive file content in chunks
                received_bytes = 0
                print(f"Receiving {filename} ({filesize} bytes) from client...")
                
                with open(filepath, 'wb') as f: # 'wb' for write binary
                    while received_bytes < filesize:
                        remaining = filesize - received_bytes
                        bytes_to_read = min(1024, remaining)
                        bytes_read = conn.recv(bytes_to_read)
                        
                        if not bytes_read:
                            break # Connection closed unexpectedly
                            
                        f.write(bytes_read)
                        received_bytes += len(bytes_read)

                if received_bytes == filesize:
                    print(f"Upload complete: {filename} saved on server.")
                    conn.sendall(b"UPLOAD_SUCCESS")
                else:
                    print(f"Upload FAILED: Only received {received_bytes}/{filesize} bytes.")
                    conn.sendall(b"UPLOAD_FAIL")
