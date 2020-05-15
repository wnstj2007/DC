import socket
import sys
import os

def sender_send(file_name, addr, port):
    sender_socket.sendto('valid list command'.encode('utf-8'), (addr, port))

    if os.path.isfile(file_name):
        sender_socket.sendto('file exists!'.encode('utf-8'), (addr, port))
        file_size = os.stat(file_name)
        print('file size in bytes:', os.stat(file_name))
        file_size = int(file_size.st_size/4096)+1
        sender_socket.sendto(file_size, (addr, port))

        with open(file_name, 'rb') as f:
            for i in range(file_size):
                print('packet number', i)
                print('data sending now')
                sender_socket.sendto(f.read(4096), (addr, port))
        print('sent all the files normally!')
    else:
        print("file doesn't exist!")
        sender_socket.sendto("file doesn't exist!".encode('utf-8'), (addr, port))

port = 8000

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.bind(('', 8000))

data, addr = sender_socket.recvfrom(2000)
data = data.split(' ')
command = data[0]

while True:
    if command == 'receive':
        file_name = data[1]
        sender_send(file_name, addr, port)
    elif command == 'exit':
        sender_socket.close()
        sys.exit()
    
    data, addr = sender_socket.recvfrom(2000)
    data = data.split(' ')
    command = data[0]