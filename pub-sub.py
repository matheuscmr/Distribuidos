import zmq
import time
import threading

global client_id

def publisher(nick):
    porta = input("Digite a a porta que deseja conectar: ")
    portas = porta.split()
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    for p in portas:
        socket.connect(f"tcp://localhost:{p}")
    

    while True:
        message = input("Digite uma mensagem: ")
        message = f'{nick}: {message}'
        socket.send_string(message)
        

def subscriber(porta):
    
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind(f"tcp://*:{porta}")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
       message = socket.recv_string()
       print(message)
         

porta, nick = input("Digite a sua porta e seu nick: ").split()

# Iniciar o subscritor
threading.Thread(target=subscriber, args=(porta)).start()

# Iniciar o publicador
threading.Thread(target=publisher, args=(porta, nick)).start()



# Aguardar o término do programa
while True:
    time.sleep(1)
