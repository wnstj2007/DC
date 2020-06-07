import socket
import sys
import os

def receive_file(file_name, addr):
    file_size, addr = receiver_socket.recvfrom(2000)
    file_size = file_size.decode('utf-8')
    header = file_size[:40]
    file_size = file_size[40:]
    sender_checksum = header[-4:]
    header = header[:-4] + '0000'
    new_checksum = checksum(header, file_size)
    print('Received checksum :',sender_checksum)
    print('New calculated checksum : 0x'+new_checksum)
    if sender_checksum != new_checksum:
        print('not matching checksum!')
        sys.exit()
    with open(file_name, 'wb') as f:
        for i in range(int(file_size)):
            print('packet number', i)
            file_data, addr = receiver_socket.recvfrom(1024)
            file_data = file_data.decode('utf-8')
            header = file_data[:40]
            file_data = file_data[40:]
            sender_checksum = header[-4:]
            header = header[:-4] + '0000'
            new_checksum = checksum(header, file_data)
            print('Received checksum :',sender_checksum)
            print('New calculated checksum : 0x'+new_checksum)
            if sender_checksum == new_checksum:
                f.write(file_data.encode('utf-8'))
            else:
                print('not matching checksum!')
                sys.exit()

def checksum(header, data):
    sum = '0000'
    #데이터와 헤더를 2byte단위로 쪼갠다.
    header = [header[i:i+2] for i in range(0, len(header), 2)]
    data = [data[i:i+2] for i in range(0, len(data), 2)]

    for i in header:
        temp = format(ord(i[0]), 'x').zfill(2)+format(ord(i[1]), 'x').zfill(2)
        print('add',temp)
        sum = format(int(temp, 16)+int(sum, 16) ,'x').zfill(4)
        #carry bit 발생 시
        if len(sum)==5:
            sum = format(int(sum[1:], 16)+int(sum[0], 16), 'x').zfill(4)

    for i in data:
        temp = format(ord(i[0]), 'x').zfill(2)+format(ord(i[1]), 'x').zfill(2)
        print('add',temp)
        sum = format(int(temp, 16)+int(sum, 16) ,'x').zfill(4)
        #carry bit 발생 시
        if len(sum)==5:
            sum = format(int(sum[1:], 16)+int(sum[0], 16), 'x').zfill(4)

    print('before :',sum)
    #sum을 이진수로 바꾼 후 0과 1을 임의의 값으로 치환했다가 다시 1, 0으로 바꾼다.
    sum = format(int(sum, 16), 'b')
    sum = sum.replace('0', 'a')
    sum = sum.replace('1', 'b')
    sum = sum.replace('a', '1')
    sum = sum.replace('b', '0')
    sum = format(int(sum, 2), 'x').zfill(4)
    print('after :',sum)
    return sum

ip_addr = '192.168.1.3'
port = 8000

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

command = input("enter a command:\n1.receive [file_name]\n2.exit\n")

while True:
    receiver_socket.sendto(command.encode('utf-8'), (ip_addr, port))
    command = command.split(' ')
    if command[0] == 'receive':
        file_name = command[1]
        receive_file(file_name, ip_addr)
    elif command[0] == 'exit':
        receiver_socket.close()
        sys.exit()
    else:
        print('wrong input')
        continue
    
    command = input("enter a command:\n1.receive [file_name]\n2.exit\n")