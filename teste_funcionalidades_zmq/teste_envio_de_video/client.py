import zmq
import cv2
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.subscribe("")

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