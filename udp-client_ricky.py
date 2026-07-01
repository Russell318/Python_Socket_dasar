import socket
 
HOST = '10.25.18.26'
PORT = 1111
 
 
def start_udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
    print(f"Client UDP berjalan, mengirim datagram ke {HOST}:{PORT}...")
 
    try:
        # Pola BERGANTIAN 1-1 (ping-pong):
        #   1) kirim SATU pesan
        #   2) tunggu & terima SATU balasan
        #   3) ulang
        while True:
            # ── 1) KIRIM satu pesan ──────────────────────────
            message = input("Masukkan pesan untuk dikirim (atau 'exit' untuk keluar): ")
            if message.lower() == 'exit':
                break
 
            client_socket.sendto(message.encode('utf-8'), (HOST, PORT))
 
            # ── 2) TERIMA satu balasan ───────────────────────
            # recvfrom() akan MENUNGGU di sini sampai satu balasan tiba,
            # baru lanjut ke pesan berikutnya. Inilah yang membuat alurnya
            # bergantian ketat: tidak bisa mengirim lagi sebelum balasan
            # untuk pesan sebelumnya diterima.
            data, addr = client_socket.recvfrom(1024)
            print(f"Menerima balasan dari server {addr}: {data.decode('utf-8')}")
 
    except KeyboardInterrupt:
        print("\nClient UDP dihentikan.")
    finally:
        client_socket.close()
 
 
if __name__ == "__main__":
    start_udp_client()