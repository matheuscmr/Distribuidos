import zmq

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:5555")

# Envio de mensagem para o Cliente B
message = "Olá Cliente B!"
socket.send(message.encode("utf-8"))

# Recebimento de resposta do Cliente B
response = socket.recv()
print(f"Cliente A recebeu a resposta: {response.decode('utf-8')}")
