#################
allow_playing = 1
enc_key = "key"

#################


import socket, select

HOST = ''
port = 50001
BUFSIZ = 1024

NUM_PORT_SOCKETS = 1

mainSock, readSock, writeSock, clientsSock = [], [], [], []
for i in range(NUM_PORT_SOCKETS):
    portSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    portSock.bind((HOST, port))
    portSock.listen(2)
    mainSock.append(portSock)
    print 'wating on ', (HOST, port)
    port += 1


def send_all_messages(writeSock):
    for messege in toSend:
        clSock, data = messege
        if clSock in writeSock:
            clSock.send(str(len(data)).zfill(4)+data)
            print "sent: ","{0:5}{1}".format(len(data),data)
            toSend.remove(messege)


def respond(data):
    if data[0:7] == "GETKEY":
        if allow_playing:
            return "ALLOWED\n" + enc_key
        return "DENIED"
    return "not recognized"




toSend = []
readSock += mainSock
while True:
    readSock, writeSock, exlst = select.select(mainSock + clientsSock, clientsSock, [])
    for manageSock in readSock:
        if manageSock in mainSock:
            (newSock, addr) = manageSock.accept()
            clientsSock.append(newSock)
            print 'connected to ', (newSock, addr)
        else:
            try:
                data = manageSock.recv(BUFSIZ)
            except socket.error, e:
                clientsSock.remove(manageSock)
            else:
                if data == '':
                    clientsSock.remove(manageSock)
                    print 'client exited'
                else:
                    toSend.append((manageSock, respond(data)))
    send_all_messages(writeSock)
