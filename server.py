# server.py - Updated for LIST and initial command handling
import socket
import os  # <-- Step 1: Import os module

HOST = '127.0.0.1'
PORT = 9000
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
