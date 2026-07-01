import socket
import threading

HOST = '127.0.0.1'
PORT = 9001

s = socket.socket()
s.connect((HOST, PORT))
name = input('Nama: ').strip() or 'Guest'
s.send(name.encode('utf-8'))


def recv():
    while True:
        data = s.recv(1024)
        if not data:
            break
        print(data.decode('utf-8'), end='')

threading.Thread(target=recv, daemon=True).start()
try:
    while True:
        msg = input()
        if msg.lower().strip() in ('/quit', 'quit', 'exit'):
            s.send(b'/quit')
            break
        s.send(msg.encode('utf-8'))
except KeyboardInterrupt:
    s.send(b'/quit')
finally:
    s.close()
    print('Keluar dari chat.')
