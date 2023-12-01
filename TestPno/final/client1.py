import socket
import ssl
from flask import Flask, render_template, request, jsonify
from getfromdb import getFromDB

host_addr = '10.46.153.254'
host_port = 8082
server_sni_hostname = 'example.com'
server_cert = 'server.crt'
client_cert = 'client1.pem'
client_key = 'client1.key'

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
app = Flask(__name__)
# Simuleer het verkrijgen van gegevens vanuit Python
def get_data(date):
    # Voer je Python-code uit om de gegevens op te halen
    data = getFromDB(date)
    #print(str(date))
    #data = [10.5, 20, 15, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125]
    #print(data)
    print("Button 1:" + str(button1))
    print("Button 2:" + str(button2))
    print("Button 3:" + str(button3))
    print("Button 4:" + str(button4))
    print("Button 5:" + str(button5))
    return data

@app.route('/get-data', methods=['GET'])
def get_data_route():
    #selected_date = request.args.get('selectedDate')
    #print(str(selected_date))
    data = get_data(selected_date)
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        global selected_date
        selected_date = request.form['selectedDate']
        
        return render_template('result.html', selectedDate=selected_date)
    return render_template('index.html')

@app.route('/run-python', methods=['GET', 'POST'])
def run_python_code():
    if request.method == 'POST':
        global selected_date
        selected_date = request.form['selectedDate']
        # Voer hier je Python-code uit en retourneer het resultaat
        #print(str(selected_date))
        global button1
        global button2
        global button3
        global button4
        global button5
        button1 = request.form.get('button1') == 'true'
        button2 = request.form.get('button2') == 'true'
        button3 = request.form.get('button3') == 'true'
        button4 = request.form.get('button4') == 'true'
        button5 = request.form.get('button5') == 'true'
        
        result = "Dit is de uitvoer van de Python-code."
        return render_template('result.html', selectedDate=selected_date, result=result)
    return render_template('index.html')


def main(): 
#host='172.20.10.3'
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
    conn.connect((host_addr, host_port))
    print("SSL established. Peer: {}".format(conn.getpeercert()))
    connected = True
    if __name__ == '__main__':
        app.run()
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

