import zmq
import time
import threading
import cv2
import numpy as np

global client_id


def publisher_mensage(portas,nick):
    
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    for p in portas:
        socket.connect(f"tcp://localhost:{p}")
    

    while True:
        message = input("Digite uma mensagem: ")
        message = f'{nick}: {message}'
        socket.send_string(message)


def publisher_video(porta):

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    for p in portas:
        socket.connect(f"tcp://localhost:{'1'+p}")
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        socket.send(frame_bytes)
        
def subscriber_mensage(porta):
    
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind(f"tcp://*:{porta}")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
       message = socket.recv_string()
       print(message)
         


def subscriber_video(porta):
    
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind(f"tcp://*:{'1'+porta}")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        frame_bytes = socket.recv()

    # Converta a sequência de bytes recebida em uma matriz numpy
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)

    # Decodifique a matriz em um quadro de imagem
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    # Exiba o quadro recebido
        cv2.imshow('Recebendo vídeo', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
         

porta_s, nick = input("Digite a sua porta e seu nick: ").split()
porta_p= input("Digite a a porta que deseja conectar: ")
portas = porta_p.split()

# Iniciar o subscritor
threading.Thread(target=subscriber_video, args=(porta_s)).start()
threading.Thread(target=subscriber_mensage, args=(porta_s)).start()

# Iniciar o publicador

threading.Thread(target=publisher_video, args=(portas)).start()
threading.Thread(target=publisher_mensage, args=(portas,nick)).start()



# Aguardar o término do programa
while True:
    time.sleep(1)
