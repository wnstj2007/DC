import socket

#server의 ip와 사용할 포트 번호 지정
ip_addr = '192.168.1.8'
port = 8000

#소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('접속 완료')

#데이터를 입력받아서 보내고, 서버로부터 데이터를 받아 출력하는 과정을 반복
while True:
	send_data = input('>>> ')
	client_socket.sendto(send_data.encode(), (ip_addr, port))

	data, addr = client_socket.recvfrom(2000)
	print(addr, ':', data.decode())
