import socket
import sys
import os

def sender_send(file_name, addr):
    if os.path.isfile(file_name):
        file_size = os.stat(file_name)
        print('file size in bytes:', file_size.st_size)
        file_size = int(file_size.st_size/984)+1
        sender_socket.sendto(str(file_size).encode('utf-8'), addr)

        with open(file_name, 'rb') as f:
            for i in range(file_size):
                print('packet number', i)
                print('data sending now')
                #헤더길이 : 8+8+4+4+2+2+4+4+4 = 40
                #1024-40 = 984
                data = f.read(984).decode('utf-8')
                header = sender_header(data, addr)
                #마지막 4byte인 checksum 값을 0에서 계산된 값으로 변경
                new_checksum = checksum(header, data)
                header = header[:-4]
                header += new_checksum
                sender_data = header + data

                sender_socket.sendto(sender_data.encode('utf-8'), addr)
        print('sent all the files normally!')
    else:
        print("file doesn't exist!")
        sys.exit()

def sender_header(data, addr):
    dst_ip, dst_port = addr
    dst_ip = list(map(int, dst_ip.split('.')))
    src_ip = '192.168.1.3' #ip주소 확인 후 수정
    src_ip = list(map(int, src_ip.split('.')))
    for i in range(4):
        dst_ip[i] = format(dst_ip[i], 'x').zfill(2)
        src_ip[i] = format(src_ip[i], 'x').zfill(2)
    dst_ip = ''.join(dst_ip)
    src_ip = ''.join(src_ip)
    dst_port = format(dst_port, 'x').zfill(4)
    src_port = format(8000, 'x').zfill(4)
    zeros = format(0, 'x').zfill(2)
    protocol = format(17, 'x').zfill(2)
    UDPLength = format(8+len(data), 'x').zfill(4)
    Length = UDPLength
    checksum = format(0, 'x').zfill(4)
    header = ''

    header += src_ip
    header += dst_ip
    header += zeros + protocol + UDPLength
    header += src_port
    header += dst_port
    header += Length
    header += checksum

    return header

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

port = 8000
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.bind(('', 8000))

data, addr = sender_socket.recvfrom(2000)
data = data.decode('utf-8').split(' ')
command = data[0]

while True:
    if command == 'receive':
        file_name = data[1]
        sender_send(file_name, addr)
    elif command == 'exit':
        sender_socket.close()
        sys.exit()
    
    data, addr = sender_socket.recvfrom(2000)
    data = data.decode('utf-8').split(' ')
    command = data[0]