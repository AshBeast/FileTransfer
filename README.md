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

## Usage

**Server**:

./server <directory_to_save_files>
**Client**:

## Test Plan

1. **Server's ability to receive and save files**:
   - Input: `./server ./test_directory` and `./client test.txt`
   - Expected Output: The content of `test.txt` is saved in `./test_directory/test.txt`.
2. **Client's ability to handle non-existent files**:

   - Input: `./client nonexistent.txt`
   - Expected Output: "File nonexistent.txt not found."

3. **Server handling multiple file transmissions**:

   - Input: `./client file1.txt file2.txt`
   - Expected Output: Both files are saved in the server-specified directory.

4. **Server shutdown using ctrl-c**:

   - Expected Output: "Shutting Down Server... Bye."

5. **Client shutdown using ctrl-c**:

   - Expected Output: "stopping client."

6. **Client handling a non-running server**:
   - Input: `./client test.txt` (without starting the server)
   - Expected Output: "Server is not running."

## Screenshots

(Note: Include visual demonstrations for each of the test cases here.)

## Notes

- Server runs continuously, accepting file transmissions until interrupted by the user.
- Client can send multiple files in a single run.
- Client provides informative feedback for errors such as missing files or server not running.
