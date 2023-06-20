import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

client_id = b"cliente2"  # Identificador único para o cliente

message = client_id + b":Oi, servidor!"
while True:
    socket.send(message)
    response = socket.recv()
    print(f"Resposta do servidor para o cliente 2: {response.decode()}")
    time.sleep(2)