import socket

HOST = '10.246.5.40'
PORT = 1234

def start_echo_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    pesan = "Halo, ini pesan dari Alfian!"
    print(f"Mengirim ke server {HOST}:{PORT}: {pesan}")
    client_socket.sendall(pesan.encode('utf-8'))

    data = client_socket.recv(1024)
    print(f"Menerima dari server: {data.decode('utf-8')}")

    client_socket.close()
    
if __name__ == "__main__":   
    start_echo_client()