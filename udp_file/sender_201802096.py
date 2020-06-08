import socket
import sys
import os

def sender_send(file_name, addr):
    if os.path.isfile(file_name):
        sequence_num = '0'
        file_size = os.stat(file_name)
        print('file size in bytes:', file_size.st_size)
        file_size = str(int(file_size.st_size/982)+1)
        header = sender_header(file_size, addr)
        new_checksum = checksum(header, file_size)
        header = header[:-4]
        header += new_checksum
        sender_data = header + file_size
        sender_socket.sendto(sender_data.encode('utf-8'), addr)
        with open(file_name, 'rb') as f:
            for i in range(int(file_size)):
                print('sending index :', sequence_num)
                #헤더길이 : 8+8+4+4+2+2+4+4+4 = 40
                #1024-40-1 = 983
                data = f.read(982).decode('utf-8')
                header = sender_header(data, addr)
                #마지막 4byte인 checksum 값을 0에서 계산된 값으로 변경
                new_checksum = checksum(header, data)
                header = header[:-4]
                header += new_checksum
                sender_data = sequence_num + header + data
                sequence_num = stopnwait(sender_data, addr)
                print('packet number', i)
                print('')

        print('sent all the files normally!')
    else:
        print("file doesn't exist!")
        sys.exit()

def stopnwait(data, addr):
    sender_socket.sendto(data.encode('utf-8'), addr)
    try:
        #data를 보내고 ack를 기다림
        receive, addr = sender_socket.recvfrom(1024)
        print('received ack index :', receive.decode('utf-8')[0])
    except socket.timeout:
        #timeout이 발생하면 data를 다시 보낸다.
        print("there's no ack")
        print('sending index :', data[0])
        ack = stopnwait(data, addr)
        #send error가 발생하면 같은 ack가 두 번 오게된다.
        #sender_socket.recvfrom(1024)
        return ack
    return receive.decode('utf-8')[0]

def sender_header(data, addr):
    dst_ip, dst_port = addr
    dst_ip = list(map(int, dst_ip.split('.')))
    src_ip = '192.168.0.8' #ip주소 확인 후 수정
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
        sum = format(int(temp, 16)+int(sum, 16) ,'x').zfill(4)
        #carry bit 발생 시
        if len(sum)==5:
            sum = format(int(sum[1:], 16)+int(sum[0], 16), 'x').zfill(4)

    for i in data:
        temp = format(ord(i[0]), 'x').zfill(2)+format(ord(i[1]), 'x').zfill(2)
        sum = format(int(temp, 16)+int(sum, 16) ,'x').zfill(4)
        #carry bit 발생 시
        if len(sum)==5:
            sum = format(int(sum[1:], 16)+int(sum[0], 16), 'x').zfill(4)

    #sum을 이진수로 바꾼 후 0과 1을 임의의 값으로 치환했다가 다시 1, 0으로 바꾼다.
    sum = format(int(sum, 16), 'b')
    sum = sum.replace('0', 'a')
    sum = sum.replace('1', 'b')
    sum = sum.replace('a', '1')
    sum = sum.replace('b', '0')
    sum = format(int(sum, 2), 'x').zfill(4)
    return sum

port = 8000
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.bind(('', 8000))
sender_socket.setblocking(False)
sender_socket.settimeout(15)

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