import socket

HOST = '127.0.0.1'
PORT = 8000

def start_echo_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Echo server aktif di {HOST}:{PORT}, menunggu koneksi...")
    conn, addr = server_socket.accept()
    print(f"Koneksi diterima dari {addr}")
    print("Saya Alserver")

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break   
            print(f"Menerima: {data.decode('utf-8')}--> Mengirim balik dari Young .....")
            conn.sendall(data)

    print("Koneksi ditutup.")
    server_socket.close()

if __name__ == "__main__":
    start_echo_server()