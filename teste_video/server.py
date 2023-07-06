import zmq
import cv2

# Criação do contexto zmq
context = zmq.Context()

# Criação do socket zmq do tipo PUB (publisher)
socket = context.socket(zmq.PUB)

# Faz o bind do socket ao endereço "tcp://*:5555"
socket.bind("tcp://*:5555")

# Inicialização do objeto para captura de vídeo da câmera (índice 0 representa a primeira câmera disponível)
video_capture = cv2.VideoCapture(0)

while True:
    # Captura um frame da câmera
    ret, frame = video_capture.read()

    # Serialize o quadro como uma sequência de bytes no formato JPEG
    frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

    # Envia o quadro para os clientes inscritos no tópico especificado
    socket.send(frame_bytes)
