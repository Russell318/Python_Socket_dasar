import socket

HOST = '10.25.18.26'
PORT = 1111

def start_udp_client():
    # socket(AF_INET, SOCK_DGRAM)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    pesan = "Halo Server UDP, ini paket datagram Alfian!"
    print(f"Mengirim ke {HOST}:{PORT} -> '{pesan}'")

    # sendto(pesan.encode(), (HOST, PORT))
    client_socket.sendto(pesan.encode('utf-8'), (HOST, PORT))

    # data, addr = recvfrom(1024)
    data, addr = client_socket.recvfrom(1024)

    # print('Echo:', data.decode())
    print(f"Echo dari server ({addr}): '{data.decode('utf-8')}'")

    # close()
    client_socket.close()

if __name__ == "__main__":
    start_udp_client()