import zmq
import cv2
import numpy as np

# Criação do contexto zmq
context = zmq.Context()

# Criação do socket zmq do tipo SUB (subscriber)
socket = context.socket(zmq.SUB)

# Conexão do socket ao endereço "tcp://localhost:5555"
socket.connect("tcp://localhost:5555")

# Configuração do socket para se inscrever em todos os tópicos
socket.subscribe("")

while True:
    # Recebe os bytes do frame do socket
    frame_bytes = socket.recv()

    # Converte a sequência de bytes recebida em uma matriz numpy
    frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)

    # Decodifica a matriz em um quadro de imagem usando cv2.imdecode()
    # cv2.IMREAD_COLOR indica que o quadro deve ser decodificado como uma imagem colorida
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    # Exibe o quadro recebido em uma janela chamada 'Recebendo vídeo' usando cv2.imshow()
    cv2.imshow('Recebendo vídeo', frame)

    # Aguarda 1 milissegundo pela tecla 'q' ser pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fecha todas as janelas abertas pelo OpenCV
cv2.destroyAllWindows()
