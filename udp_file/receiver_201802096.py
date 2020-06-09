import socket
import sys
import os
import time

#전송 오류와 송신 오류를 설정하는 변수
#상황에 맞게 True로 변경하여 사용
send_error = False
receive_error = False

def receive_file(file_name, addr):
    old_frame = ''
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
    print('')
    with open(file_name, 'wb') as f:
        for _ in range(int(file_size)):
            old_frame = receive_data(f, old_frame)

def receive_data(f, old_frame):
    global send_error, receive_error
    file_data, addr = receiver_socket.recvfrom(1024)
    file_data = file_data.decode('utf-8')
    new_frame = file_data[0]
    header = file_data[1:41]
    file_data = file_data[41:]
    print('received frame number :', new_frame)
    sender_checksum = header[-4:]
    header = header[:-4] + '0000'
    new_checksum = checksum(header, file_data)
    print('Received checksum :',sender_checksum)
    print('New calculated checksum : 0x'+new_checksum)
    #이전에 받은 프레임과 현재 받은 프레임이 같으면 바로 ack를 전송하고 다음 패킷을 받음
    if old_frame == new_frame:
        if receive_error == True:
            print('ack is lost!')
            receive_error = False
        stopnwait(new_frame+header+file_data, addr)
        send_error = False
        new_frame = receive_data(f, new_frame)
        return new_frame
    stopnwait(new_frame+header+file_data, addr, send_error, receive_error)
    if sender_checksum == new_checksum:
        f.write(file_data.encode('utf-8'))
    else:
        print('not matching checksum!')
        sys.exit()
    return new_frame

def stopnwait(data, addr, send_error=False, receive_error=False):
    if data[0] == '1':
        next_frame = '0'
    elif data[0] == '0':
        next_frame = '1'
    data = next_frame+data[1:]
    print('send ack number :', next_frame)

    if send_error == True:
        time.sleep(17)
    if receive_error == True:
        receiver_socket.sendto(data.encode('utf-8'), ('127.0.0.1', 8000))
    else:
        receiver_socket.sendto(data.encode('utf-8'), addr)
    print('')

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

ip_addr = '192.168.0.8'
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