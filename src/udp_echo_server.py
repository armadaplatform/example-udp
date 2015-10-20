import socket

UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

listen_addr = ("", 200)
UDPSock.bind(listen_addr)

while True:
    data, addr = UDPSock.recvfrom(1024)
    print(data.strip(), addr)
    UDPSock.sendto('Reply from server: {}'.format(data), addr)
