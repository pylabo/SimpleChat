'''Server for multithreaded (asynchronous) chat application.'''
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from random import randint


def accept_incoming_connections():
    '''Sets up handling for incoming clients.'''
    while True:
        client, client_address = SERVER.accept()
        print('i {}:{} has connected.'.format(client_address[0],client_address[1]))
        client.send(bytes('i Enter your name to join.', 'utf8'))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    '''Handles a single client connection.'''

    name = client.recv(BUFSIZ).decode('utf8')
    welcome = 'i Welcome {}. Send "/leave" to exit.'.format(name)
    client.send(bytes(welcome, 'utf8'))
    self.lstjonmsg = ['i {} has joined! You must construct additional pylons.'.format(name),
                            'i {} just slid into the server.'.format(name),
                      'i Never gonna give {} up. Never gonna let {} down.'.format(name,name)]
    broadcast(bytes(self.lstjonmsg[randint(0,len(self.lstjonmsg))],'utf8'))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes('/leave', 'utf8'):
            broadcast(msg, name + ': ')
        else:
            client.send(bytes('/leave', 'utf8'))
            client.close()
            del clients[client]
            broadcast(bytes('i {} has left the chat.'.format(name),'utf8'))
            break


def broadcast(msg, prefix=''):  # prefix is for name identification.
    '''Broadcasts a message to all the clients.'''

    for sock in clients:
        sock.send(bytes(prefix, 'utf8') + msg)


clients = {}
addresses = {}

host = ''
port = 1710
BUFSIZ = 1024
ADDR = (host, port)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == '__main__':
    print('  SimpleChat Server 0.1.0 Canary')
    SERVER.listen(5)
    print('i Listening @ {}:{}'.format('localhost',port))
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
