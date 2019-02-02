import socket,os

HOST = '172.18.12.253'
PORT = 50001
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpCliSock.connect(ADDR)

data = \
    """GET /game.exe HTTP/1.1
Host: 192.168.1.134
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Accept: */*
Referer: 
Accept-Encoding: gzip, deflate
Accept-Language: en-US"""
tcpCliSock.send(data)

n_data=""
r_data = tcpCliSock.recv(BUFSIZ)
n_data+=r_data
while r_data:
    r_data = tcpCliSock.recv(BUFSIZ)
    print " - ",r_data
    n_data += r_data
print "exit loop"
tcpCliSock.close()
f = open("E:\cyber\project2\POC\Client\gclient_game.exe", "w")

f.write(n_data)
f.close()
print len(n_data)
