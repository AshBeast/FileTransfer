# Client-Server Program Using Domain Sockets

This program establishes a client-server system that communicates through UNIX domain sockets. The client sends files to the server, which in turn saves these received files into a specific directory.

## Table of Contents

- [Features](#features)
- [Design](#design)
  - [Server (`server.py`)](#server-serverpy)
  - [Client (`client.py`)](#client-clientpy)
- [Setup](#setup)
- [Usage](#usage)
- [Test Plan](#test-plan)
- [Screenshots](#screenshots)
- [Notes](#notes)

## Features

- Client communicates file details (name, size, content) to the server.
- Server saves received files to a specified directory.
- Graceful shutdown on both client and server with proper resource cleanup.
- Error handling for scenarios like missing files or server not running.

## Design

### Server (`server.py`)

**Functions**:

1. `__init__` (in `File` class) - Initializes a File object with a name and content.
2. `save` (in `File` class) - Saves the content of the file to a specified directory.
3. `signal_handler` - Handles the SIGINT signal for graceful shutdown.
4. `clearSocket` - Removes the domain socket file if it exists to ensure a clean startup.

### Client (`client.py`)

**Function**:

1. `signal_handler` - Handles the SIGINT signal, informs the server about the client's exit and ensures graceful shutdown.

## Setup

1. Clone this repository.
2. Navigate to the directory containing the program files.
3. You will need 2 terminals at this directory one to run the server and one client

## Usage

**Server**:
python3 server.py <directory_to_save_files>

**Client**:
python3 client.py <name of 1 or more files>

## Test Plan

1. **Server's ability to receive and save files**:

   - Input: `python3 server.py ./test_directory` and `python3 client.py test.txt`
   - Expected Output: The content of `test.txt` is saved in `./test_directory/test.txt`.
     ![Test Txt](Screenshots/testTxt.png)

   - Input: `python3 client.py mountain.jpeg`
   - Expected Output: The image `mountain.jpeg` is saved in `./test_directory/mountain.jpeg`.
     ![Image](Screenshots/imageTest.png)

   - Input: `python3 client.py paint.jpg client.py`
   - Expected Output: The content of `paint.jpg` and `client.py` is saved in `./test_directory/paint.jpg` and `./test_directory/client.py`.
     ![More than One File](Screenshots/morethanOneFile.png)

2. **Client's ability to handle non-existent files**:

   - Input: `python3 client.py nonexistent.txt`
   - Expected Output: "File nonexistent.txt not found." and the server will look for the next client
     ![No File](Screenshots/nofile.png)

3. **Client shutdown using ctrl-c**:

   - Input: `python3 client.py` without arguments
   - control-c
   - Expected Output: "stopping client."
     ![Kill Client](Screenshots/killclient.png)

4. **Server shutdown using ctrl-c**:

   - Expected Output:
     "Shutting Down Server...

   Bye."
   ![Kill Server](Screenshots/killServer.png)

5. **Client handling a non-running server**:
   - Input: `python3 client.py test.txt` (without starting the server)
   - Expected Output: "Server is not running."
     ![Client without Server](Screenshots/clientwithoutserver.png)

## Notes

- Server runs continuously, accepting file transmissions until interrupted by the user.
- Client can send multiple files in a single run.
- Client provides informative feedback for errors such as missing files or server not running.
- If the client is give no files in the argument, the client will ask the user once for files to input
- Files that already exist in the directory will be overwritten
