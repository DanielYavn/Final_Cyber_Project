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
            clSock.send(data)
            clSock.send("")
            clSock.send("")
            toSend.remove(messege)



def respond(data):
    GET_request(data)
    if data[0:7] == "GETKEY":

        return str(1)
    return "not recognized"

def GET_request(data):
    import re
    print re.findall(r'GET (.*) HTTP',data)




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
                print data
            except socket.error, e:
                clientsSock.remove(manageSock)
            else:
                if data == '':
                    clientsSock.remove(manageSock)
                    print 'client exited'
                else:
                    toSend.append((manageSock, respond(data)))
    send_all_messages(writeSock)
