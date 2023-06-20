import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    client_id, client_message = message.split(b":", 1)  # Divide a mensagem em identificador do cliente e conteúdo

    print(f"Mensagem recebida do cliente {client_id.decode()}: {client_message.decode()}")

    # Processa a mensagem do cliente e envia uma resposta
    response = b"Recebido pelo servidor"
    socket.send(response)