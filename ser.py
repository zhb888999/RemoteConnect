import os
import threading
import sys
import termios
import pty
import subprocess
import signal
import time
import socket

kill = False

def cout(fd, ser):
    global kill
    while True:
        try:
            out = os.read(fd, 1024)
            if out:
                print(out)
                ser.send(out)
            time.sleep(0.01)
        except OSError:
            break
        except UnicodeDecodeError:
            break
    kill = True

def cin(fd, ser):
    global kill
    while True:
        try:
            os.write(fd, ser.recv(1024))
            print("cin")
        except OSError:
            break
        except UnicodeEncodeError:
            break
    kill = True

def handle_SIGCHLD(signum, frame):
    global kill
    print("disconnect")
    kill = True

while True:
    pid, fd = os.forkpty()
    if pid == 0:
        subprocess.run(["login"])
    else:
        s = socket.socket()
        s.connect(('192.168.102.10',1234))
        s.send('ser'.encode())
        if s.recv(1024).decode() != "succ":
            print('connect error!')
            break
        signal.signal(signal.SIGCHLD, handle_SIGCHLD)
        t1 = threading.Thread(target=cout, args=(fd,s), daemon=True)
        t2 = threading.Thread(target=cin, args=(fd,s), daemon=True)
        t1.start()
        t2.start()
        print("waite")
        while not kill:
            time.sleep(0.1)