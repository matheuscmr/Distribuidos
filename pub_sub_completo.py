import zmq
import time
import threading
import cv2
import numpy as np
import pyaudio

# Função para publicar mensagens
def publisher_mensagem(ip_t, nick):
    # Criação do contexto zmq
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    # Conexão aos IPs dos assinantes
    for ip in ip_t:
        porta = "7000"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)

    while True:
        # Solicita ao usuário que digite uma mensagem
        message = input("Digite uma mensagem: ")
        message = f'{nick}: {message}'

        # Envio da mensagem para os assinantes
        socket.send_string(message)

# Função para publicar vídeo
def publisher_video(ip_t):
    # Criação do contexto zmq
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    # Conexão aos IPs dos assinantes
    for ip in ip_t:
        porta = "7001"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)

    # Captura de vídeo a partir da câmera
    video_capture = cv2.VideoCapture(0)

    while True:
        # Captura de um frame do vídeo
        ret, frame = video_capture.read()

        # Codificação do frame como uma sequência de bytes no formato JPG
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

        # Envio do frame para os assinantes
        socket.send(frame_bytes)

# Função para publicar áudio
def publisher_audio(ip_t):
    # Criação do contexto zmq
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    # Conexão aos IPs dos assinantes
    for ip in ip_t:
        porta = "7002"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)

    # Configuração dos parâmetros de áudio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    while True:
        # Leitura dos dados de áudio do fluxo de entrada
        data = stream.read(CHUNK)

        # Envio dos dados de áudio para os assinantes
        socket.send(data)

# Função para receber mensagens
def subscriber_mensagem(ip):
    # Criação do contexto zmq
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    # Configuração do socket para se inscrever em todas as mensagens
    porta = "7000"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        # Recebimento de uma mensagem
        message = socket.recv_string()

        # Exibição da mensagem recebida
        print(message)

# Função para receber vídeo
def subscriber_video(ip):
    # Criação do contexto zmq
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    # Configuração do socket para se inscrever em todos os tópicos   
    porta = "7001"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        # Recebimento dos bytes do frame de vídeo
        frame_bytes = socket.recv()

        # Conversão dos bytes para uma matriz numpy
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)

        # Decodificação da matriz em um frame de imagem usando cv2.imdecode()
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

        # Exibição do frame recebido
        cv2.imshow('Recebendo vídeo', frame)

        # Verificação da tecla 'q' para interromper a exibição
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fechamento das janelas abertas pelo OpenCV
    cv2.destroyAllWindows()

# Função para receber áudio
def subscriber_audio(ip):
    # Criação do contexto zmq
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    # Configuração do socket para se inscrever em todos os tópicos
    porta = "7002"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)

    # Configuração dos parâmetros de áudio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    while True:
        # Recebimento dos dados de áudio
        data = socket.recv()

        # Reprodução dos dados de áudio no fluxo de saída
        stream.write(data)

# Solicitação do IP do usuário
ip_s = input("Digite o seu IP: ")

# Solicitação do nick do usuário
nick = input("Digite o seu nick: ")

# Solicitação dos IPs dos assinantes
ip_t = input("Digite os IPs que deseja conectar: ").split()

# Iniciar os subscritores em threads separadas
threading.Thread(target=subscriber_mensagem, args=(ip_s,)).start()
threading.Thread(target=subscriber_video, args=(ip_s,)).start()
threading.Thread(target=subscriber_audio, args=(ip_s,)).start()

# Aguardar um tempo para garantir que os subscritores estejam ativos
time.sleep(1)

# Iniciar os publicadores em threads separadas
threading.Thread(target=publisher_mensagem, args=(ip_t, nick)).start()
threading.Thread(target=publisher_video, args=(ip_t,)).start()
threading.Thread(target=publisher_audio, args=(ip_t,)).start()

# Manter o programa em execução até ser interrompido manualmente
while True:
    pass