import socket
import threading

HOST = '127.0.0.1'
PORT = 9000

clients = []
usernames = {}

lock = threading.Lock()


def broadcast(message, sender_socket=None):
    with lock:
        for client in clients:
            try:
                if client != sender_socket:
                    client.send(message)
            except Exception:
                if client in clients:
                    clients.remove(client)
                if client in usernames:
                    del usernames[client]


def send_message(target_socket, message):
    try:
        target_socket.send(message.encode('utf-8'))
    except Exception:
        with lock:
            if target_socket in clients:
                clients.remove(target_socket)
            if target_socket in usernames:
                del usernames[target_socket]


def handle_client(client_socket, address):
    try:
        name_data = client_socket.recv(1024).decode('utf-8').strip()
        if not name_data:
            client_socket.close()
            return

        username = name_data
        with lock:
            usernames[client_socket] = username
        print(f"[SERVER] {username} terhubung dari {address}")
        broadcast(f"[SERVER] {username} bergabung ke chat.".encode('utf-8'), client_socket)

        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            decoded = message.decode('utf-8')
            if decoded.lower().strip() in ('/quit', 'quit', 'exit'):
                break
            formatted = f"{username}: {decoded}"
            print(f"[CHAT] {formatted}")
            broadcast(formatted.encode('utf-8'), client_socket)

    except ConnectionResetError:
        pass
    finally:
        with lock:
            if client_socket in clients:
                clients.remove(client_socket)
            left_name = usernames.pop(client_socket, 'Unknown')
        print(f"[SERVER] {left_name} keluar.")
        broadcast(f"[SERVER] {left_name} meninggalkan chat.".encode('utf-8'), client_socket)
        client_socket.close()


def server_console_input():
    print("[SERVER] Ketik pesan untuk broadcast atau gunakan perintah berikut:")
    print("  /all pesan           -> kirim ke semua client")
    print("  /user nama pesan     -> kirim ke client tertentu")
    print("  /list                -> lihat daftar client")
    print("  /quit                -> hentikan server")

    while True:
        try:
            command = input()
        except EOFError:
            break

        if not command:
            continue

        if command.strip().lower() == '/quit':
            print('[SERVER] Perintah keluar diterima. Hentikan server dengan Ctrl+C.')
            break

        if command.strip().lower() == '/list':
            with lock:
                print('[SERVER] Client terhubung:')
                for sock, name in usernames.items():
                    print(f' - {name}')
            continue

        if command.startswith('/all '):
            message = command[len('/all '):].strip()
            if message:
                formatted = f"[SERVER] {message}"
                print(f"[SERVER] Broadcast: {message}")
                broadcast(formatted.encode('utf-8'))
            continue

        if command.startswith('/user '):
            rest = command[len('/user '):].strip()
            parts = rest.split(' ', 1)
            if len(parts) < 2:
                print('[SERVER] Format: /user nama pesan')
                continue
            target_name, message = parts
            target_socket = None
            with lock:
                for sock, name in usernames.items():
                    if name == target_name:
                        target_socket = sock
                        break
            if target_socket:
                formatted = f"[SERVER] {message}"
                send_message(target_socket, formatted)
                print(f"[SERVER] Pesan dikirim ke {target_name}: {message}")
            else:
                print(f"[SERVER] Client dengan nama '{target_name}' tidak ditemukan.")
            continue

        print('[SERVER] Perintah tidak dikenali. Gunakan /all, /user, /list, atau /quit.')


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[SERVER] Chat server berjalan di {HOST}:{PORT}")

    input_thread = threading.Thread(target=server_console_input, daemon=True)
    input_thread.start()

    try:
        while True:
            client_socket, address = server_socket.accept()
            with lock:
                clients.append(client_socket)
            thread = threading.Thread(target=handle_client, args=(client_socket, address), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Server dihentikan.")
    finally:
        with lock:
            for client in clients:
                client.close()
        server_socket.close()


if __name__ == '__main__':
    start_server()
