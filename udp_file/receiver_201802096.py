import socket
import sys
import os

def receive_file(file_name, addr, port):
    data, addr = receiver_socket.recvfrom(2000)
    if data != 'valid list command':
        print('not valid command')

    file_exist, addr = receiver_socket.recvfrom(2000)
    if file_exist != "file doesn't exist!":
        print(data)
        return None

    file_size, addr = receiver_socket.recvfrom(2000)
    with open(file_name, 'wb') as f:
        for i in range(file_size):
            print('packet number', i)
            file_data, addr = receiver_socket.recvfrom(4096)
            f.write(file_data)

ip_addr = '192.168.1.8'
port = 8000

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.setblocking(False)
receiver_socket.settimeout(15)

command = input("enter a command:\n1.receive[file_name]\n2.exit\n")

while True:
    receiver_socket.sendto(command.encode('utf-8'), (ip_addr, port))
    command = command.split(' ')
    if command[0] == 'receive':
        file_name = command[1]
        receive_file(file_name, ip_addr, port)
    elif command[0] == 'exit':
        receiver_socket.close()
        sys.exit()
    else:
        print('wrong input')
        continue
    
    command = input("enter a command:\n1.receive[file_name]\n2.exit\n")