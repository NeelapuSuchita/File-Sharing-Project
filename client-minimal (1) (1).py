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

# --- Day 4: Implement UPLOAD command (Client to Server) ---
            elif command.startswith("UPLOAD"):
                # 1. Parse filename and prepare to receive the size header
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

def upload_file(s, filename):
    """Sends UPLOAD command and transmits file to the server."""
    # Assuming file to upload is in CLIENT_DOWNLOADS directory
    filepath = os.path.join(CLIENT_DOWNLOAD_DIR, filename) 
    
    try:
        filesize = os.path.getsize(filepath)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found locally for upload.")
        return

    # 1. Send the UPLOAD command
    s.sendall(f"UPLOAD {filename}".encode())

    # Wait for server ACK
    ack = s.recv(1024).decode().strip()
    if ack != "READY_FOR_UPLOAD":
        print(f"Upload failed: Server not ready. Response: {ack}")
        return

    # 2. Send the file size header (Crucial)
    size_header = str(filesize).zfill(10).encode() 
    s.sendall(size_header)

    # 3. Send the file content in chunks
    print(f"\nUploading {filename} ({filesize} bytes) to server...")
    with open(filepath, 'rb') as f: # 'rb' for read binary
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break # File transmission is done
            s.sendall(bytes_read)

    # 4. Receive final success/fail message
    final_status = s.recv(1024).decode().strip()
    if final_status == "UPLOAD_SUCCESS":
        print(f"Upload complete: {filename} successfully saved on server.")
    else:
        print(f"Upload failed. Server response: {final_status}")

# client.py - Day 5: Login Function
def login(s, username, password):
    """Sends LOGIN command and checks server response."""
    print(f"\nAttempting to log in as {username}...")
    
    command = f"LOGIN {username} {password}"
    s.sendall(command.encode())
    
    # Receive the server response
    response = s.recv(1024).decode().strip()
    
    if response == "LOGIN_SUCCESS":
        print("Login Successful!")
        return True
    else:
        print(f"Login Failed. Server response: {response}")
        return False
