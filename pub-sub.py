import zmq
import time
import threading

def publisher():
    porta = input("Digite a a porta que deseja conectar: ")
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect(f"tcp://localhost:{porta}")
    

    while True:
        message = input("Digite uma mensagem: ")
        socket.send_string(message)
        

def subscriber():
    porta = input("Digite a sua porta: ")
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind(f"tcp://*:{porta}")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
       message = socket.recv_string()
       print(f"Mensagem recebida: {message}")
         

# Iniciar o subscritor
threading.Thread(target=subscriber).start()

# Iniciar o publicador
threading.Thread(target=publisher).start()



# Aguardar o término do programa
while True:
    time.sleep(1)
