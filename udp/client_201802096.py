import socket

ip_addr = '192.168.1.8'
port = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('접속 완료')

while True:
	send_data = input('>>> ')
	client_socket.sendto(send_data.encode(), (ip_addr, port))

	data, addr = client_socket.recvfrom(2000)
	print(addr, ':', data.decode())
