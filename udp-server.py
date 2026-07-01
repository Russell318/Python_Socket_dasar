import socket

HOST = 'localhost'
PORT = 9000

def start_udp_server():
    # socket(AF_INET, SOCK_DGRAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # bind((HOST, PORT))
    server_socket.bind((HOST, PORT))
    print(f"UDP Echo Server aktif di {HOST}:{PORT}, menunggu datagram...")

    # loop:
    while True:
        try:
            # data, addr = recvfrom(1024)
            data, addr = server_socket.recvfrom(1024)
            print(f"Menerima datagram dari client: {data.decode('utf-8')}")

            # sock.sendto(data, addr) # echo
            print(f"Mengirim balik (echo) ke client")
            server_socket.sendto(data, addr)

        except KeyboardInterrupt:
            print("\nServer dimatikan.")
            break

    server_socket.close()

if __name__ == "__main__":
    start_udp_server()
