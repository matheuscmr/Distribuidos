import zmq

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:5555")

# Recebimento da mensagem do Cliente A
message = socket.recv()
print(f"Cliente B recebeu a mensagem: {message.decode('utf-8')}")

# Envio de resposta para o Cliente A
response = "Olá Cliente A! Recebi sua mensagem."
socket.send(response.encode("utf-8"))
