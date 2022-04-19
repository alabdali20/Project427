# Arranged and modified for CIS 427
# John P. Baugh, Ph.D. (original - January 2022)
# server.py - the server

#More info - https://docs.python.org/3/howto/sockets.html
import select
import socket
from math import pi
import sys
import threading

PORT_NUM = 3433
NUM_REQUESTS_ALLOWED = 5
NUM_BYTES = 1024
# is_login = False
# user_name = ""
dictionary = {}


# connect using
# AF_INET - the Address Family for Internet (IPv4)
# SOCK_STREAM - TCP as the transport protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), PORT_NUM))

#only queue up to 5 (set 1 if allowing only only at a time)
server_socket.listen(NUM_REQUESTS_ALLOWED)


#Pre: The function receive the "SOLVE" command for either the rectangle and the cricle.
#Post: The function return the result in a string
def solve(message):
    command = message.split()
    try:
        # Cricle
        if command[1] == '-c':
            # Check the radius in case it is cricle
            if len(command) == 2:
                solution_msg = "Error: No radius found"
                return solution_msg, 4
            elif len(command) == 3:
                radius = int(command[2])
                circumference = 2 * pi * radius
                area = pi * radius * radius
                circumference = "{:.2f}".format(circumference)
                area = "{:.2f}".format(area)
                solution_msg = f"Circle's circumference is {circumference} and area is {area}"
                return solution_msg, 1
            else:
                solution_msg = f"301 Message format error"
                return solution_msg, 0
        # Rectangle
        elif command[1] == '-r':
            # Check the sides in case it is rectangle
            if len(command) == 2:
                solution_msg = "Error: No sides found"
                return solution_msg, 4
            elif len(command) == 3:
                side = int(command[2])
                perimeter = 4 * side
                area = side * side
                perimeter = "{:.2f}".format(perimeter)
                area = "{:.2f}".format(area)
                solution_msg = f"Rectangle's perimeter is {perimeter} and area is {area}"
                return solution_msg, 2
            elif len(command) == 4:
                side = int(command[2])
                length = int(command[3])
                perimeter = (2 * side) + (2 * length)
                area = side * length
                perimeter = "{:.2f}".format(perimeter)
                area = "{:.2f}".format(area)
                solution_msg = f"Rectangle's perimeter is {perimeter} and area is {area}"
                return solution_msg, 3
            else:
                solution_msg = "301 Message format error"
                return solution_msg, 0
        else:
            solution_msg = "300, Invalid Command"
            return solution_msg, 0
    except:
        solution_msg = "300, Invalid Command"
        return solution_msg, 0


#Pre: The function receive the "LIST" command and the user name
#Post: The function read user file and return the result in a string. If the user is root, and he command "-all" the result will be all the files
def list(message, user_name):
    command = message.split()
    if len(command) == 1:
        f = open(f"{user_name}_solutions.txt", "r")
        list_msg = f'{user_name}\n{f.read()}'
        f.close()
        return list_msg
    elif (len(command) == 2) and (command[1] == "-all"):
        if user_name == "root":
            list_msg = read_all_files()
            return list_msg
        else:
            list_msg = "Error: you are not the root user"
            return list_msg
    else:
        list_msg = "301 Message format error"
        return list_msg


#Pre: The function recieved to read all files without any parameter.
#Post: The function read all the files and then return a string of all the data. If the file exist read it, otherwise write 'No interactions yet'.
def read_all_files():
    all_files_msg = ""
    with open('logins.txt', 'r') as file1:
        for line in file1.readlines():
            line = line.split()
            try:
                f = open(f'{line[0]}_solutions.txt', 'r')
                if f.read() == "":
                    raise
                f.seek(0)
                all_files_msg += f'{line[0]}\n'
                all_files_msg += f.read()
                f.close()
            except:
                all_files_msg += f'{line[0]}\nNo interactions yet\n'
    return all_files_msg


def login(message):
    try:
        global dictionary
        command = message.split()
        # Check if the user is allow to join the server or not
        with open('logins.txt', 'r') as file1:
            for line in file1.readlines():
                line = line.split()
                if (command[1] == line[0]) and (command[2] == line[1]):
                    if command[1] in dictionary:
                        login_message = f'The user {command[1]} is already logged in!'
                        file1.close()
                        return login_message
                    else:
                        login_message = "SUCCESS"
                        return login_message
            else:
                login_message = "FAILURE: Please provide correct username and password. Try again."
                file1.close()
                return login_message
    except:
        login_message = "300, Invalid Command"
        return login_message


def handle(client_socket):
    is_login = False
    global dictionary
    try:
        while True:
            message = client_socket.recv(NUM_BYTES)
            message = message.decode("utf-8")
            command = message.split()
            if (command[0] == 'LOGIN') and (is_login is not True):
                login_message = login(message)
                if login_message == "SUCCESS":
                    is_login = True
                    user_name = command[1]
                    dictionary.update({user_name:client_socket})

                client_socket.send(bytes(login_message, "utf-8"))

            elif is_login is True:
                f = open(f"{user_name}_solutions.txt", "a")
                # Check 'SOLVE' command
                if command[0] == 'SOLVE':
                    solve_msg, flag = solve(message)
                    if flag == 1:
                        f.write(f"Radius {command[2]}: {solve_msg}\n")
                        client_socket.send(bytes(solve_msg, "utf-8"))
                    elif flag == 2:
                        f.write(f"Sides {command[2]} {command[2]}: {solve_msg}\n")
                        client_socket.send(bytes(solve_msg, "utf-8"))
                    elif flag == 3:
                        f.write(f"Sides {command[2]} {command[3]}: {solve_msg}\n")
                        client_socket.send(bytes(solve_msg, "utf-8"))
                    elif flag == 4:
                        f.write(f"{solve_msg}\n")
                        client_socket.send(bytes(solve_msg, "utf-8"))
                    else:
                        client_socket.send(bytes(solve_msg, "utf-8"))
                elif command[0] == 'LIST':
                    list_msg = list(message, user_name)
                    client_socket.send(bytes(list_msg, "utf-8"))
                elif (command[0] == 'LOGOUT') or (command[0] == 'SHUTDOWN'):
                    is_login = False
                    client_socket.send(bytes("200 OK", "utf-8"))
                    client_socket.close()
                    f.close()
                    if command[0] == 'SHUTDOWN':
                        sys.exit()
                        break
                    else:
                        del dictionary[user_name]
                        break
                elif command[0] == 'MESSAGE':
                    chat(client_socket, message, user_name)
                else:
                    client_socket.send(bytes("300, Invalid Command", "utf-8"))

            else:
                handle_message = "300, Invalid command"
                client_socket.send(bytes(handle_message, "utf-8"))

    except:
        handle_message = "Errorrrrrrr"
        client_socket.send(bytes(handle_message, "utf-8"))


def chat(client_socket, message, user_name): # add , user_name
    global dictionary
    try:
        command = message.split()
        if user_name == 'root' and command[1] == '-all':
            user_list = []
            for client in dictionary:
                if client != 'root':
                    user_list.append(client)
                    to_client = dictionary.get(client)
                    chat_message = f"Message from {user_name}:\n{' '.join(command[2:])}"
                    to_client.send(bytes(chat_message, "utf-8"))
            print(f'Message from {user_name}:\n'
                  f"{' '.join(command[2:])}\n"
                  f"Sending to {', '.join(user_list[:])}\n")
            helper = "Message sent!"
            client_socket.send(bytes(helper, "utf-8"))

        elif command[1] in dictionary: # check if the user is logged in
            to_client = dictionary.get(command[1])
            if to_client == client_socket: # check if the user want to be smart and send a message to himself
                helper = "Cant send message to yourself!"
                client_socket.send(bytes(helper, "utf-8"))
            else: #other than than, send the message to the client
                chat_message = f"Message from {user_name}:\n{' '.join(command[2:])}"
                print(f'Message from {user_name}:\n'
                      f"{' '.join(command[2:])}\n"
                      f'Sending to {command[1]}\n')
                to_client.send(bytes(chat_message, "utf-8"))
                helper = "Message sent!"
                client_socket.send(bytes(helper, "utf-8"))
        elif command[1] not in dictionary and command[1] != '-all': # check if the user doesn't exist in the logged in dictionary
            lines = []
            with open('logins.txt', 'r') as file1:
                for line in file1.readlines():
                    line = line.split()
                    lines += line
            if command[1] in lines: # if the name is in the register textfile, but to logged in
                helper = f"User {command[1]} is not logged in"
                print(f'Message from {user_name}:\n'
                      f"{ ' '.join(command[2:])}\n"
                      f'Sending to {command[1]}\n'
                      f'{command[1]} is not logged in.\n'
                      f'Informing client\n')
                client_socket.send(bytes(helper, "utf-8"))
            else: # if the name is not in the register textfile
                helper = f"User {command[1]} does not exist"
                print(f'Message from client:\n'
                      f"{ ' '.join(command[2:])}\n"
                      f'Sending to {command[1]}\n'
                      f"User {command[1]} doesn't exist.\n"
                      f'Informing client\n')
                client_socket.send(bytes(helper, "utf-8"))
        else:
            helper = '301, Message format error'
            client_socket.send(bytes(helper, "utf-8"))

    except:
        helper = "Somethings went wrong!"
        client_socket.send(bytes(helper, "utf-8"))


# threads_arr = []
#now start the connection/communication loop
while True:
    client_socket, address = server_socket.accept()
    print(f"Connection established with client at {address}")
    client_socket.send(bytes("Server connection established!", "utf-8"))



    # threads_arr.append(t)
    t = threading.Thread(target=handle, args=(client_socket,))
    t.start()
    # print(f'Active Clients {threading.active_count() - 1}')