"""Script for t GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
import tkinter.ttk as ttk

class client():
    def __init__(self):
        self.host = None
        self.port = None
        self.root = Toplevel()
        self.root.title('SimpleChat - {}:{}'.format(self.host,self.port))
        self.frmmsg = Frame(self.root)
        self.sbrmsgmsg = ttk.Scrollbar(self.frmmsg)
        self.lstmsgmsg = Listbox(self.frmmsg,height=15,width=100,yscrollcommand=self.sbrmsgmsg.set,font='monospace 10')
        self.sbrmsgmsg.pack(side=RIGHT, fill=Y)
        self.lstmsgmsg.pack(side=LEFT, fill=BOTH)
        self.lstmsgmsg.pack()
        self.frmmsg.pack()
        self.entmsg = Entry(self.root)
        self.entmsg.bind('<Return>', self.send)
        self.entmsg.pack(fill=X)
        self.btnsnd = Button(self.root, text='Send', command=self.send)
        self.btnsnd.pack(side=LEFT)
        self.root.protocol('WM_DELETE_WINDOW',self.userClose)
        self.BUFSIZ = None
        self.connectAddress = (None,None)
    def receive(self,event=None):
        """receive
        Handles message receiving."""
        while True:
            try:
                self.lstmsgmsg.insert(END,self.client_socket.recv(self.BUFSIZ).decode('utf8'))
            except OSError:
                break

    def send(self,event=None):
        """Handles sending of messages."""
        msg = self.entmsg.get()
        self.entmsg.delete('0',END)
        self.entmsg.insert(END, 'Sending...')
        self.client_socket.send(bytes(msg,'utf8'))
        self.entmsg.delete('0',END)
        if msg == '/leave':
            self.client_socket.close()
            self.root.destroy()

    def userClose(self,event=None):
        """userClose
        Handles closing procedure"""
        self.entmsg.delete('0',END)
        self.entmsg.insert(END,'/leave')
        self.send()
    def engine(self):
        print('  SimpleChat Client 0.1.5 Canary')
        self.host = input('? Host ')
        self.port = input('? Port ')
        if not self.host:
            print('i No host specified')
            print('i Exit @ code 1')
            exit(1)
        if not self.port:
            print('i No port specified')
            print('i Exit @ code 2')
            exit(2)
        else:
            self.port = int(self.port)
        self.BUFSIZ = 1024
        self.connectAddress = (self.host,self.port)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.connectAddress)
        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()
        self.root.title('SimpleChat - {}:{}'.format(self.host, self.port))
        self.root.mainloop()

x = client()
x.engine()
