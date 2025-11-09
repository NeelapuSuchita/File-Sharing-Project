# client.py - Complete implementation (Day 1 to Day 5)
import socket
import os
import sys

# --- Network Configuration (Day 1) ---
HOST = '127.0.0.1'
PORT = 9000
CLIENT_DOWNLOAD_DIR = 'CLIENT_DOWNLOADS' 

# Ensure the download directory exists
os.makedirs(CLIENT_DOWNLOAD_DIR, exist_ok=True)
print(f"Client will save files to: {CLIENT_DOWNLOAD_DIR}")

# --- Day 5: Login Function ---
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

# --- Day 3: Download Function (Server to Client) ---
def download_file(s, filename):
    """Requests file from server and receives it reliably."""
    
    # 1. Send DOWNLOAD command
    print(f"\nRequesting file: {filename}")
    s.sendall(f"DOWNLOAD {filename}".encode())

    # 2. Receive the file size header (10 bytes)
    # The server sends a 10-byte zero-padded size.
    size_header = b''
    while len(size_header) < 10:
        chunk = s.recv(10 - len(size_header))
        if not chunk:
            print("Error: Server closed connection while waiting for size header.")
            return
        size_header += chunk
        
    try:
        filesize = int(size_header.decode())
    except ValueError:
        print("Error: Received non-integer size header from server.")
        return

    if filesize == 0:
        print(f"Error: File '{filename}' not found on server or file is empty.")
        return

    # 3. Receive file content in chunks
    filepath = os.path.join(CLIENT_DOWNLOAD_DIR, filename)
    received_bytes = 0
    print(f"Receiving {filename} ({filesize} bytes)...")
    
    try:
        with open(filepath, 'wb') as f: # 'wb' for write binary
            while received_bytes < filesize:
                remaining = filesize - received_bytes
                bytes_to_read = min(1024, remaining)
                bytes_read = s.recv(bytes_to_read)
                
                if not bytes_read:
                    # This happens if connection closes unexpectedly before receiving full file
                    break 
                    
                f.write(bytes_read)
                received_bytes += len(bytes_read)

        if received_bytes == filesize:
            print(f"Download complete: {filename} saved successfully.")
        else:
            print(f"Download FAILED: Only received {received_bytes}/{filesize} bytes.")

    except Exception as e:
        print(f"Error during file write: {e}")

# --- Day 4: Upload Function (Client to Server) ---
def upload_file(s, filename):
    """Sends UPLOAD command and transmits file to the server."""
    
    # We assume the file to upload is in the CLIENT_DOWNLOADS directory for simple testing
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
    with open(filepath, 'rb') as f:
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


# --- Main Client Execution (Day 1, Day 2, Day 5) ---
def run_client():
    """Connects to server, handles login, and executes file operations."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print("Error: Could not connect to server. Is the server running?")
            sys.exit(1)
            
        # 1. Receive initial greeting from server
        greeting = s.recv(1024).decode().strip()
        print("Server said:", greeting)
        
        # --- Day 5: Perform Login ---
        # NOTE: Using 'admin' and 'securepwd' which must match the server's VALID_USERS
        login_successful = login(s, "admin", "securepwd") 
        
        if login_successful:
            print("\n--- Starting Authenticated Operations ---")
            
            # --- Day 2: Send LIST command and display response ---
            print("\n--- Testing LIST command ---")
            s.sendall(b"LIST") 
            list_data = s.recv(4096).decode().strip() # Increased buffer for large file lists
            print("Files available on server:\n", list_data)

            # --- TESTING DOWNLOAD (Day 3) ---
            # IMPORTANT: UNCOMMENT AND CHANGE 'test_file.txt' to a file that exists in your SERVER_FILES folder!
            # download_file(s, "test_file.txt") 
            
            # --- TESTING UPLOAD (Day 4) ---
            # IMPORTANT: UNCOMMENT AND CHANGE 'uploaded_test.txt' to a file that exists in your CLIENT_DOWNLOADS folder!
            # upload_file(s, "uploaded_test.txt") 
            
        else:
            print("\n--- Aborting operations due to failed login. ---")
            
        print("\nClient closing connection.")

if __name__ == '__main__':
    run_client()
