# student name: Tobechi Onwenu

import socket
import sys
import threading

size = 1024  # receive buffer size
users = {}  # Store usernames and passwords in a dictionary
clients = {}  # Keep track of connected clients
lock = threading.Lock()  # Lock for synchronization

def get_username_by_conn(conn):
    with lock:
        for username, client_conn in users.items():
            if client_conn == conn:
                return username
    return None

def handle_client(conn):
    # Receive the username from the client
    try:
        login_name = conn.recv(size).decode()

        # Check if the username is already in the users dictionary
        with lock:
            if login_name in users:
                # Send a message to the client that the user exists
                conn.send("EXISTING".encode())

                # Receive the password from the client
                login_password = conn.recv(size).decode()

                # Check if the password matches the one stored in the users dictionary
                if login_password == users[login_name]:
                    # Send a message to the client that the login is successful
                    conn.send("SUCCESS".encode())
                else:
                    # Send a message to the client that the password is incorrect
                    conn.send("FAILURE".encode())
                    conn.close()
                    return
            else:
                # Send a message to the client to enter a new password
                conn.send("NEW".encode())

                # Receive the new password from the client
                password_n = conn.recv(size).decode()

                # Store the username and password in the users dictionary
                users[login_name] = password_n

                # Send a message to the client that the registration is successful
                conn.send("Registration successful. Welcome to the chat room!".encode())

        # Add the client socket to the clients dictionary
        with lock:
            clients[login_name] = conn
        print("Currently logged in: {}".format(login_name))
        print("Awaiting message...")

        # Loop forever to receive and process messages from the client
        while True:
            # Receive a message instruction from the client
            message = conn.recv(size).decode()

            # Check if the message is an operation command (PM, DM, or EX)
            if message == "PM":
                conn.send("BROADCAST".encode())

                # Extract the public message
                public_message = conn.recv(size).decode()

                # Broadcast the public message to all other clients in the chat room
                with lock:
                    for username, client_conn in clients.items():
                        if client_conn != conn:
                            server_message = "{}: {}".format(login_name, public_message).encode()
                            client_conn.send(server_message)

                # Send a confirmation message to the client that the message was sent
                conn.send("SUCCESS".encode())
            elif message == "DM":
                conn.send("DIRECT_MESSAGE".encode())

                # Send the list of currently logged-in clients to the client
                with lock:
                    logged_in_clients = "\n".join(clients.keys())
                conn.send(logged_in_clients.encode())

                # Extract the recipient and the direct message from the message string
                target_user = conn.recv(size).decode()
                direct_message = conn.recv(size).decode()

                # Find the socket of the recipient in the clients dictionary
                with lock:
                    recipient_conn = clients.get(target_user, None)

                # Send the direct message to the recipient only if found
                if recipient_conn:
                    recipient_conn.send("{}: {}".format(login_name, direct_message).encode())
                    conn.send("SUCCESS".encode())
                else:
                    conn.send("FAILURE".encode())
            elif message == "EX":
                # Send a goodbye message to the client
                conn.send("Goodbye. See you next time.".encode())

                # Remove the client socket from the clients dictionary
                with lock:
                    clients.pop(login_name)

                # Close the connection with the client
                conn.close()
                return
    except ConnectionError as e:
        print("Error handling client connection:", e)

def start_server(argv):
    host = '127.0.0.1'
    port = int(sys.argv[1])

    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(3)
        print("Listening on port:", port)

        while True:
            # Accept a connection from a client
            try:
                client, addr = server_socket.accept()
                print("Connection from", addr, "has been established.")
                # Start a new thread to handle the client
                threading.Thread(target=handle_client, args=(client,)).start()

            except (socket.error, ConnectionAbortedError) as e:
                print("Error accepting client connection:", e)
                continue

    except socket.error as e:
        print("Error binding server socket:", e)

    except KeyboardInterrupt:
        print("Server is shutting down...")

    finally:
        server_socket.close()

start_server(sys.argv[1:])
