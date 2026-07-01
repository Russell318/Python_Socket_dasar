import socket
import threading

HOST = '127.0.0.1'
PORT = 9000
USERNAME = 'Gamma'


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print('[CLIENT] Koneksi diputus oleh server.')
                break
            print(message)
        except ConnectionResetError:
            print('[CLIENT] Koneksi terputus.')
            break
        except Exception:
            break


def send_messages(client_socket):
    while True:
        message = input()
        if message.lower().strip() in ('/quit', 'quit', 'exit'):
            client_socket.send(message.encode('utf-8'))
            break
        client_socket.send(message.encode('utf-8'))


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(USERNAME.encode('utf-8'))
    print(f'[CLIENT] Terhubung sebagai {USERNAME}. Ketik pesan lalu tekan Enter. Ketik /quit untuk keluar.')

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    receive_thread.start()

    send_messages(client_socket)
    client_socket.close()
    print('[CLIENT] Keluar dari chat.')


if __name__ == '__main__':
    start_client()
