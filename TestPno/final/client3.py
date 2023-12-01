import socket
import ssl

host_addr = '127.0.0.1'
host_port = 8082
server_sni_hostname = 'example.com'
server_cert = 'server.crt'
client_cert = 'client3.pem'
client_key = 'client3.key'

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
    conn.connect((host_addr, host_port))
    print("SSL established. Peer: {}".format(conn.getpeercert()))
    connected = True
    
    while connected:
        msg = input("> ")

        conn.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        else:
            msg = conn.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")

if __name__ == "__main__":
    main()