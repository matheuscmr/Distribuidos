import zmq
import time
import threading
import cv2
import numpy as np
import pyaudio

def subscriber_mensagem(ip_t):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    if (type(ip_t)==str):
        new_ip=[]
        new_ip.append(ip_t)
        ip_t = new_ip
    for ip in ip_t:
        porta = "7000"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)
    while True:
        message = socket.recv_string()
        print(message)
        


def subscriber_video(ip_t):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    
    for ip in ip_t:
        porta = "7001"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)
    if (type(ip_t)==str):
        new_ip=[]
        new_ip.append(ip_t)
        ip_t = new_ip
    while True:
        frame_bytes = socket.recv()
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        cv2.imshow('Recebendo video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

    
def subscriber_audio(ip_t):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    if (type(ip_t)==str):
        new_ip=[]
        new_ip.append(ip_t)
        ip_t = new_ip

    for ip in ip_t:
        porta = "7002"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)
        socket.subscribe("")

    audio = pyaudio.PyAudio()
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    stream = audio.open(format=FORMAT,channels=CHANNELS,rate=RATE,output=True)

    while True:
            audio_data = socket.recv()
            stream.write(audio_data)


def publisher_mensagem(ip,nick):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    porta = "7000"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)
    
    while True:
        message = input("Digite uma mensagem: ")
        message = f'{nick}: {message}'
        socket.send_string(message)


    

def publisher_video(ip):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    porta = "7001"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)



    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        socket.send(frame_bytes)


def publisher_audio(ip):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    porta = "7002"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)
    audio = pyaudio.PyAudio()
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    while True:
        audio_data = stream.read(CHUNK)
        socket.send(audio_data)

ip_t = input("Digite o seu ip: ")
nick = input("Digite o seu nick: ")
ip_s = input("Digite os IPs que deseja conectar: ").split()

# Iniciar os subscritores
threading.Thread(target=subscriber_mensagem, args=(ip_s)).start()
threading.Thread(target=subscriber_video, args=(ip_s,)).start()
threading.Thread(target=subscriber_audio, args=(ip_s,)).start()

# Aguardar um tempo para garantir que os subscritores estão ativos
time.sleep(1)

# Iniciar os publicadores
threading.Thread(target=publisher_mensagem, args=(ip_t,nick)).start()
threading.Thread(target=publisher_video, args=(ip_t,)).start()
threading.Thread(target=publisher_audio, args=(ip_t,)).start()

# Manter o programa em execução até ser interrompido manualmente
while True:
    pass
