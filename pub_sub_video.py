import zmq
import time
import threading
import cv2
import numpy as np

global client_id

def publisher():
    porta = input("Digite a a porta que deseja conectar: ")
    portas = porta.split()
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    for p in portas:
        socket.connect(f"tcp://localhost:{p}")
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        socket.send(frame_bytes)
        

def subscriber(porta):
    
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind(f"tcp://*:{porta}")
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
         

porta = input("Digite a sua porta: ")

# Iniciar o subscritor
threading.Thread(target=subscriber, args=(porta)).start()

# Iniciar o publicador
threading.Thread(target=publisher).start()



# Aguardar o término do programa
while True:
    time.sleep(1)
