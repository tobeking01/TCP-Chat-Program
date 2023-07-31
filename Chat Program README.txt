student name: Tobechi Onwenu

Chat Program README

1. Files Present in the Directory:
server.py - This file contains the server-side code for the chat application. It handles user registration, login, and communication between clients.
client.py - This file contains the client-side code for the chat application. It allows users to interact with the server and send/receive messages to/from other clients.
Makefile - This file contains the compilation instructions for the server and client code. It simplifies the build process.
README.md - You are currently reading this file. It provides an overview of the directory contents, instructions to compile and run the code, and other relevant information.

2. Imports used:
import socket
import sys
import threading


3. Running the server:
make run_server PORT=<PORT_NUMBER>
Replace <PORT_NUMBER> with the desired port number for the server to listen on (e.g., 5000).


Running the client:
make run_client SERVER=<SERVER_IP> PORT=<PORT_NUMBER> USERNAME=<USERNAME>
Replace <SERVER_IP> with the IP address of the machine running the server (e.g., 127.0.0.1 if running locally), <PORT_NUMBER> with the same port number used for the server, and <USERNAME> with the desired username for the client.



4. Usage Instructions:
Once the server and clients are running, you can use the following commands in the client to interact with the chatroom:
'PM': Send a public message to all users in the chatroom.
'DM': Send a direct message to a specific user in the chatroom.
'EX': Exit the chatroom.

5. Termination:
To terminate the server, press Ctrl + C in the terminal or command prompt where the server is running.
That's it! You should now have the server and client up and running, ready to chat in the chatroom. Enjoy chatting with your friends!


6. How the Code Works:
The chat application consists of a server and multiple clients. The server acts as a central hub for communication between clients.
When a client starts, it connects to the server and provides a username. If the username is already registered, the client provides the password to log in. Otherwise, a new password is set for the new user.
Once logged in, clients can send public messages to all other users or send direct messages to specific users.
The server maintains two dictionaries: users to store usernames and passwords, and clients to keep track of connected clients.
A threading.Lock() is used to protect shared resources (users and clients) from concurrent access and potential race conditions.
The code also uses conditional variables and semaphores to avoid deadlocks and ensure threads do not hold multiple locks simultaneously.
When a client wants to exit the chat, it sends the "EX" message to the server, which then handles the disconnection gracefully.

7. Please see screenshot for how the code works.