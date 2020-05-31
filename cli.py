import socket
import sys
import threading
import termios
    

def cin(s):
    while True:
        s.send(sys.stdin.read(1).encode())
def cout(s):
    while True:
        sys.stdout.write(s.recv(1024).decode())
        sys.stdout.flush()


host_post = ('192.168.102.10', 1234)
s = socket.socket()
s.connect(host_post)
s.send('cli'.encode())
t = s.recv(1024).decode()
print(t)
if t == 'succ':
    sin = sys.stdin.fileno()
    old = termios.tcgetattr(sin)
    new = termios.tcgetattr(sin)
    new[3] = new[3] & ~termios.ECHO
    new[3] = new[3] & ~termios.ICANON
    termios.tcsetattr(sin, termios.TCSADRAIN, new)
    t1 = threading.Thread(target=cin, args=(s,))
    t2 = threading.Thread(target=cout, args=(s,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
