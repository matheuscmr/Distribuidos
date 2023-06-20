import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

client_id = b"cliente1"  # Identificador único para o cliente

message = client_id + b":Ola, servidor!"
while True:
    socket.send(message)
    response = socket.recv()
    print(f"Resposta do servidor para o cliente 1: {response.decode()}")
    time.sleep(2)