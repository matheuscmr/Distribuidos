import zmq
import time
import threading
import cv2
import numpy as np
import pyaudio

def publisher_mensagem(ip_t, nick):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    for ip in ip_t:
        porta = "7000"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)

    while True:
        message = input("Digite uma mensagem: ")
        message = f'{nick}: {message}'
        socket.send_string(message)

def publisher_video(ip_t):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    for ip in ip_t:
        porta = "7001"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        socket.send(frame_bytes)

def publisher_audio(ip_t):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    for ip in ip_t:
        porta = "7002"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        socket.send(data)

def subscriber_mensagem(ip):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    porta = "7000"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        message = socket.recv_string()
        print(message)

def subscriber_video(ip):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    porta = "7001"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        frame_bytes = socket.recv()
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        cv2.imshow('Recebendo video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def subscriber_audio(ip):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    porta = "7002"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    while True:
        data = socket.recv()
        stream.write(data)

ip_s = input("Digite o seu ip: ")
nick = input("Digite o seu nick: ")
ip_t = input("Digite os IPs que deseja conectar: ").split()

# Iniciar os subscritores
threading.Thread(target=subscriber_mensagem, args=(ip_s,)).start()
threading.Thread(target=subscriber_video, args=(ip_s,)).start()
threading.Thread(target=subscriber_audio, args=(ip_s,)).start()

# Aguardar um tempo para garantir que os subscritores estão ativos
time.sleep(1)

# Iniciar os publicadores
threading.Thread(target=publisher_mensagem, args=(ip_t, nick)).start()
threading.Thread(target=publisher_video, args=(ip_t,)).start()
threading.Thread(target=publisher_audio, args=(ip_t,)).start()

# Manter o programa em execução até ser interrompido manualmente
while True:
    pass
