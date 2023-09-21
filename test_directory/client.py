import socket
import sys
import signal

SOCKET_FILE = './domain_socket.sock'

def signal_handler(sig, frame):
    print('stopping client')
    client.sendall("/Done".encode('utf-8'))
    client.close()
    sys.exit(0)        

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.settimeout(10.0)

# Register the signal_handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Ensure the server is running
try:
    client.connect(SOCKET_FILE)
except socket.timeout:
    print("Timed out while waiting for server connection")
    client.close()
except socket.error:
    print("Server is not running.")
    sys.exit(1)

# Check for file arguments
filenames = []
if len(sys.argv) < 2:
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
            print("Received: ", client.recv(1024).decode('utf-8'))

            # Send file size
            client.sendall((str(len(contents)) + "\n").encode('utf-8'))
            print("Received: ", client.recv(1024).decode('utf-8'))
            
            # Send file contents
            client.sendall(contents)
            print("Received: ", client.recv(1024).decode('utf-8'))
            print("-----------------------------------------------")
            
    except socket.timeout:
        print("Timed out while waiting for server response.")
        client.close()
        sys.exit(1)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        continue
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}")
        continue

client.sendall("/Done".encode('utf-8'))
client.close()