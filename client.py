# Arranged and modified for CIS 427
# John P. Baugh, Ph.D. (original - January 2022)
# client.py - the client

import socket

PORT_NUM = 3433
NUM_BYTES = 1024
is_login = False
is_logout = False
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), PORT_NUM))

#established command
message = client_socket.recv(NUM_BYTES)
message = message.decode("utf-8")
print(message)

#login commands
while (is_login == False):
    msg = input('C: ')
    client_socket.send(bytes(msg, "utf-8"))
    login_statue = client_socket.recv(NUM_BYTES)
    login_statue = login_statue.decode("utf-8")
    if(login_statue == 'SUCCESS'):
        is_login = True
        print(f'S: {login_statue}')
    else:
        print(f'S: {login_statue}')


#other commands
while (is_login == True):
    msg = input('C: ')
    if ((msg.find("LOGOUT") == 0) or (msg.find("SHUTDOWN") == 0)):
        is_logout = True
    client_socket.send(bytes(msg, "utf-8"))
    command = client_socket.recv(NUM_BYTES)
    command = command.decode("utf-8")
    print(f'S: {command}')
    if (is_logout):
        client_socket.close()
        break