# TCP-Chat-Program
Implement the client and server sides of an "online chat room" application. Either TCP or UDP can be used. In this application, the client determines the operation to be performed: public messaging or direct messaging. Even though only one port is being used, the server should accept multiple simultaneous client connections. The server should respond appropriately to the specific command send by the client. The specifics of the protocol are detailed below.

Type of Messages
There are two types of message frames: 1) data message and 2) command message. A data message is exchanged between clients (i.e., the Public and Direct messages described in the following online chat room protocol). A command message is exchanged between a client and the server (e.g., operation, acknowledgment, confirmation messages described below). Define the message format to encode the message type. For example, the first character of the message can be used to distinguish between the two types of messages (e.g., "C" for command message and "D" for data message). 
 
Note: The sender is responsible for encoding the type of information into the message frame. The receiver is responsible for extracting the type of information from the message and performs accordingly. (Refer to the Technical Instruction section for more details.)

Online Chat Room Protocol
The server opens a port, creates the TCP/UDP socket, goes into the "wait for connection" state, and actively listens for socket connections. Hint: Please read the Technical Instruction Section below for details.
The client logs into the system by connecting to the server on the appropriate port.
The client sends the username.
The server checks whether it is a new user or an existing user and requests a password. Note: Store usernames and passwords in a file rather than in memory (otherwise, the credentials will get lost once the server program is terminated).
The client sends the password.
The server either registers a new user or checks to see if the password matches. The server then sends the acknowledgment to the client.
Note: multiple clients should be able to register at the same time.
The server continues to wait for an operation command from a client or a new client connection.
The client goes into the "prompt user for operation" state and prompts the user for operation.
The client passes operation (PM: Public Message, DM: Direct Messaging, EX: Exit) to the server.
Operation is executed as follows:
PM: 
The client sends an operation (PM) to broadcast a public message to all active clients (i.e., the clients who successfully log in to the system but have not exited yet).
The server sends the acknowledgment back to the client to prompt for the message to be sent.
The client sends the broadcast message to the server.
The server receives the message and sends it to all other clients. Note: The server should keep track of the socket descriptors it has created for each client since the program began running. You can decide how to implement this tracking function.
The server sends confirmation that the message was sent. Note: You can decide the content/format of the confirmation.
The client receives the confirmation message.
The client returns to the "prompt user for operation" state, and the server returns to the "wait for operation from client" state.
DM:
The client sends the operation (DM) to send a message to a specific client.
The server sends the list of currently online users. Note: The server should keep track of all online users. You can decide how to implement this tracking function. We assume that any client can go offline by using operation (EX).
The client receives the list of online users from the server.
The client prompts the user to select the username of the target user.
The client sends the target username and the message to the server.
The server receives the above information and checks to make sure the target user exists/online.
If the target user is online, the server forwards the message to the user. The server should do this by sending the message to the corresponding socket descriptor of the target user.
The target user receives the message and displays it. 
The server sends confirmation that the message was sent or that the user did not exist. Note: You can decide the content/format of the confirmation.
The client receives the confirmation message from the server.
The client returns to the "prompt user for operation" state, and the server returns to the "wait for operation from client" state.
EX:
The client sends operation (EX) to close its connection with the server and end the program.
The server receives the operation and closes the socket descriptor for the client.
The server updates its tracking record on the socket descriptors of active clients and usernames of online users.
The client should close the socket.

Note: If it is not explicitly specified, the client and server will return to the "prompt user for operation" and "wait for operation from client" state, respectively, after a successful operation and wait for the next operation.

Technical Instructions
Multithread Server: The server must be able to monitor and handle messages from multiple clients simultaneously. This can be done using multiprocessing or multithreading. It is recommended to use pthread library if you are programming using C or threading if you are using Python. You will need a main thread to listen to all new connections. This can be done using the socket accept function within a while loop. This main thread is just your main program. You will need to create a new thread for each connected client. You can set a threshold (e.g., maxThreadNumber=10) for the total number of threads. A multithreaded server implementation example can be found here. Also, you may review https://youtu.be/Pg_4Jz8ZIH4
 Multithread Client: The client must also handle concurrent messages from multiple origins (e.g., command messages from the server and data messages from other clients). This should be done using multithreading as well. In particular, each client should have one thread (e.g., thread1) to collect all messages from the socket and another thread (e.g., thread2) to parse and react to those messages. Note that the main program itself is a thread, so you only need to create one extra thread. The client will also need to identify the type of messages it received and perform appropriately based on the application protocol. E.g., if a data message is received, the client prints out the message; if a command message is received, the client should continue the interaction with the server based on the command message. 
  Note: when using the (EX) command to exit, make sure all threads are properly terminated. Specifically, you should terminate the main thread after the extra thread has finished its job. This can be done by using the pthread_join() method. 
  To ensure multithreading is working correctly on both client and server, you can perform the following simple tests:
Try logging/registering with multiple clients with the server at the same time. One client's login process should not block any other clients.
Reach a state where a server is prompting client 1 to type in some message (e.g., after client 1 sends a BM command). Then send a private message to client 1 from client 2. Client 1 should first print out the message from client 2 and then return to the prompt state.
 Note: A simple test scenario of your implementation: three clients and one server. You can run three clients on three different machines and run the server on any of the three machines where you run the clients or on a fourth machine. You also can run all the clients and the server on the same machine. You can then test broadcast messaging, private messaging, and multithreading in this scenario. 
General Notes
Your code may be written in C or python3. You should create separate files in your submission, a set of server files for the server code and a set of client files for the client code. Each directory should contain a Makefile for building your code appropriately, if you are using C.
The endian-ness matters. Review https://youtu.be/OoHich9BPxg.
To determine the size of files, you may want to use the fseek (or equivalent ifstream operation) function and/or the peek operation. For efficiency reasons, you probably should not "roll your own."
When in doubt, you may add extra print-out statements to assist with debugging. Make sure to disable your debugging output before handing in the assignment.
You can connect back to localhost (127.0.0.1), which will allow you to test your code on the same machine where you have the server running. Run a separate terminal session and then run the client code by connecting to localhost.
When compiling the code, remember to link the libraries -lpthread.
Server Side Design
The server is responsible for handling the connection request from multiple clients, processing the request, then looping back to handle further requests from any client. The server should listen on the specified port number (that is assigned to you) that is given by the command-line argument. Your server should bind to the port and then listen for incoming client connections. You may decide if you would like to allow timeouts for better responsiveness, but any timeout is purely optional. You may want to allow for port reuse for quicker recovery after a crash.

 Once a new client request arrives, your server should use the accept function to create a new client socket.

The server executable should be named chatserver and be invoked as follows:

./chatserver Port

Client Side Design
The client is responsible for initiating a connection to a server. Once connected, the client code should prompt the user for an operation (BM, PM, EX) and transmit the operation to the server. 


 The client executable should be named chatclient and be invoked as follows:

./chatclient Server_Name Port Username

 The first argument is the server's hostname to connect to (this will depend on what machine you start your server code on). The second argument is the port number. The third argument is the username for login.
