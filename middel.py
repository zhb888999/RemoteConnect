import socket
import threading
import time

mess = {'ser':None, 'cli':None}

def cli(c):
    global mess
    if mess['ser'] is None:
        c.send('error'.encode('utf-8'))
        c.close()
        return
    while True:
        m = c.recv(1024)
        if m:
            print(m)
        mess['ser'].send(m)


def ser(c):
    global mess
    while mess['cli'] is None:
        time.sleep(0.1)
    while True:
        mess['cli'].send(c.recv(1024))

host_post = ('192.168.102.10', 1234)
s = socket.socket()
s.bind(host_post)
s.listen(2)
while True:
    c, addr = s.accept()
    print("connect!")
    t = c.recv(1024).decode()
    if t == 'ser':
        print("ser!")
        mess['ser'] = c
        c.send('succ'.encode())
        threading.Thread(target=ser, args=(c,)).start()
    if t == 'cli':
        print("cli!")
        mess['cli'] = c
        c.send('succ'.encode('utf-8'))
        threading.Thread(target=cli, args=(c,)).start()

