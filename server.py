import socket
import os
import sys
import signal

SOCKET_FILE = './domain_socket.sock'
SAVE_DIRECTORY = ""

# Add this at the top of your server.py
if len(sys.argv) < 2:
    print("Please provide a directory to save files into.")
    sys.exit(1)
SAVE_DIRECTORY = sys.argv[1]

class File:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def save(self, directory=SAVE_DIRECTORY):
        # Ensure the directory exists, create if it doesn't
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the content to the file
        with open(os.path.join(directory, self.name), 'wb') as f:
            f.write(self.content)

# Handle SIGINT
def signal_handler(sig, frame):
    print('\nShutting Down Server...')
    clearSocket()
    server.close()
    print('\nBye')
    sys.exit(0)

# Register the signal_handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Ensure socket file does not already exist
def clearSocket():
    if os.path.exists(SOCKET_FILE):
        os.remove(SOCKET_FILE)

clearSocket()

# Create a UNIX socket
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_FILE)
server.listen(1)

while True:
    print("Server waiting for connection...")
    conn, addr = server.accept()
    print("Connected.")

    while True: 
        # Receive filename
        filename = conn.recv(1024).decode('utf-8').strip()
        if (filename == "/Done"):
            break

        print(f"Receiving data for file: {filename}")
        conn.sendall(b"server has file name")
        
        # Receive file size
        file_size = int(conn.recv(1024).decode('utf-8').strip())
        print(f"Expected file size: {file_size} bytes")
        conn.sendall(b"server has file size")

        # Receive file contents and saving the file
        data = b""
        while len(data) < file_size:
            packet = conn.recv(file_size - len(data))
            if not packet:
                break
            data += packet
        print("Received file data")
        my_file = File(filename, data)
        my_file.save()
        conn.sendall(b"Files received by server! and saved")
    conn.close()
