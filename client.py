import socket
import sys
import signal

SOCKET_FILE = './domain_socket.sock'

def signal_handler(sig, frame):
    print('stopping client')
    client.sendall("/Done".encode('utf-8'))
    client.close()
    sys.exit(0)

def serverCheck():
    try:
        client.connect(SOCKET_FILE)
    except socket.error:
        print("Server is not running.")
        sys.exit(1)


client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Register the signal_handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Ensure the server is running
serverCheck()

# Check for file arguments
filenames = []
if len(sys.argv) < 2:
    print("Please provide one or more file names as arguments.")
    filenames = input("Please provide one or more file names: ").split()
else:
    filenames = sys.argv[1:]

# Read and send file contents
for filename in filenames:
    try:
        with open(filename, 'rb') as f:
            contents = f.read()
            
            # Send filename
            client.sendall((filename + "\n").encode('utf-8'))
            print(client.recv(1024))

            # Send file size
            client.sendall((str(len(contents)) + "\n").encode('utf-8'))
            print(client.recv(1024))
            
            # Send file contents
            client.sendall(contents)
            print(f"Sent contents of {filename} to server.")
            response = client.recv(1024)
            print("Received:", response.decode('utf-8'))
            
    except FileNotFoundError:
        print(f"File {filename} not found.")
        continue
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}")
        break

client.sendall("/Done".encode('utf-8'))
client.close()