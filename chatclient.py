# student name: Tobechi Onwenu

import socket
import sys
import threading

size = 1024  # receive buffer size

def receive_messages(client):
    while True:
        try:
            server_message = client.recv(size).decode()
            if not server_message:
                break
            print(server_message)
        except ConnectionError:
            print("Connection to server lost.")
            break

def prompt_user(client):
    try:
        while True:
            message = input("['PM' Public Message, 'DM' Direct Messaging, 'EX' Exit]\nWhat operation would you like to perform? ")
            client.send(message.encode())

            reply = client.recv(size).decode()

            if reply == "BROADCAST":
                public_message = input("Enter your message: ")
                client.send(public_message.encode())
            elif reply == "DIRECT_MESSAGE":
                logged_in_clients = client.recv(size).decode()  # Print the list of currently logged-in clients
                print(logged_in_clients)
                target_user = input("Enter the username of the target user: ")
                direct_message = input("Enter your message: ")
                client.send(target_user.encode())
                client.send(direct_message.encode())
            elif reply == "SUCCESS":
                print("Your message was sent.")
            elif reply == "FAILURE":
                print("The user does not exist or is offline.")
            elif reply == "Goodbye. See you next time.":
                print("Goodbye. See you next time.")
                client.close()
                break
            else:
                print(reply)
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (client window closed)
        print("\nLogging off...")
        client.send("EX".encode())
    finally:
        client.close()

def connect_to_server(argv):
    host, port, name = sys.argv[1:]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, int(port)))
        print("Connected to server")
    except (socket.error, ConnectionRefusedError) as e:
        print("Unable to connect to the server:", e)
        return

    username = input("Enter your username: ")
    client.send(username.encode())
    print("Awaiting status...")

    status = client.recv(size).decode()
    print(status)

    if status == "EXISTING":
        password = input("Enter your password: ")
        client.send(password.encode())
        login = client.recv(size).decode()
        print(login)
        if login == "SUCCESS":
            print("Login successful. Welcome to the chat room, {}".format(username))
        else:
            print("Wrong password. Please try again.")
            client.close()
            return
    elif status == 'NEW':
        print("Welcome new user to the chat room!")
        password_n = input("Enter your new password here: ")
        client.send(password_n.encode())
        login_n = client.recv(size).decode()
        print(login_n)

    threading.Thread(target=receive_messages, args=(client,)).start()
    prompt_user(client)

if __name__ == "__main__":
    connect_to_server(sys.argv[1:])
