import socket
import threading

HOST = '127.0.0.1'
PORT = 9001
clients = []


def broadcast(msg, sender=None):
    for c in clients:
        if c != sender:
            try:
                c.send(msg)
            except:
                clients.remove(c)


def handle(c):
    name = c.recv(1024).decode('utf-8').strip()
    if not name:
        c.close()
        return
    clients.append(c)
    broadcast(f"[SERVER] {name} bergabung\n".encode(), c)
    c.send(f"[SERVER] Selamat datang, {name}!\n".encode())
    while True:
        data = c.recv(1024)
        if not data or data.strip() == b'/quit':
            break
        broadcast(f"{name}: {data.decode()}".encode(), c)
    clients.remove(c)
    broadcast(f"[SERVER] {name} keluar\n".encode(), c)
    c.close()


def server_input():
    while True:
        try:
            msg = input()
        except EOFError:
            break
        if not msg.strip():
            continue
        if msg.lower().strip() in ('/quit', 'quit', 'exit'):
            print('[SERVER] Selesai mengirim pesan.')
            break
        broadcast(f"[SERVER]: {msg}\n".encode())

s = socket.socket()
s.bind((HOST, PORT))
s.listen()
print(f"Chat server berjalan di {HOST}:{PORT}")
threading.Thread(target=server_input, daemon=True).start()
try:
    while True:
        c, _ = s.accept()
        threading.Thread(target=handle, args=(c,), daemon=True).start()
except KeyboardInterrupt:
    pass
finally:
    s.close()
