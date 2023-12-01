import socket
import threading
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl
import time
led_pin = 17

listen_addr = '10.46.153.254'
listen_port = 8082
server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'combined_certs3.pem'

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
TURN_ON_MSG = "TURN ON"
TURN_OFF_MSG = "TURN OFF"

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    conn = context.wrap_socket(conn, server_side=True)
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] {msg}")
        # msg = f"Msg received: {msg}"
        msg = f"Msg received: {msg}"
        conn.send(msg.encode(FORMAT))

    conn.close()

def main():
    print("[STARTING] Server is starting...")
    bindsocket = socket.socket()
    bindsocket.bind((listen_addr, listen_port))
    bindsocket.listen()

    print(f"[LISTENING] Server is listening on {listen_addr}:{listen_port}")
    while True:
        conn, addr = bindsocket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()