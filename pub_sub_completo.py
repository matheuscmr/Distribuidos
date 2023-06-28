import zmq
import time
import threading
import cv2
import numpy as np
import pyaudio
global client_id


def publisher_mensage(ip_t,nick):
    
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    if (type(ip_t)==str):
        new_ip=[]
        new_ip.append(ip_t)
        ip_t = new_ip
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
    if (type(ip_t)==str):
        new_ip=[]
        new_ip.append(ip_t)
        ip_t = new_ip

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
  
    chunk = 1024
    channels = 1
    sample_rate = 44100

    audio = pyaudio.PyAudio()

    if (type(ip_t)==str):
        new_ip=[]
        new_ip.append(ip_t)
        ip_t = new_ip

    for ip in ip_t:
        porta = "7002"
    
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)
    stream = audio.open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk)
    while True:
        audio_data = stream.read(chunk)
        socket.send(audio_data)

 
    stream.stop_stream()
    stream.close()
    socket.close()
    context.term()


def subscriber_mensage(ip):
    
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    porta = "7000"
    ip_complete = "tcp://"+ip+":"+porta
    socket.bind(ip_complete)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
       message = socket.recv_string()
       print(message)
         


def subscriber_video(ip):
    
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    porta = "7001"
    ip_complete = "tcp://"+ip+":"+porta

    socket.bind(ip_complete)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        frame_bytes = socket.recv()

    # Converta a sequência de bytes recebida em uma matriz numpy
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)

    # Decodifique a matriz em um quadro de imagem
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    # Exiba o quadro recebido
        cv2.imshow('Recebendo video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def subscriber_audio(ip):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    porta = "7002"
    ip_complete = "tcp://"+ip+":"+porta
    chunk = 1024
    channels = 1
    sample_rate = 44100
    audio = pyaudio.PyAudio()
    socket.bind(ip_complete)
    stream = audio.open(format=pyaudio.paInt16,channels=channels,rate=sample_rate,output=True,frames_per_buffer=chunk)
    while True:
        audio_data = socket.recv()
        stream.write(audio_data)

    stream.stop_stream()
    stream.close()
    socket.close()
    context.term()

ip_s = input("Digite o seu ip: ")
nick = input("digite o seu nick: ")
ip_t= input("Digite os ips que deseja conectar: ")
ip = ip_t.split() 
if (type(ip_s)==str):
    new_ip=[]
    new_ip.append(ip_s)
    ip_s = new_ip
if (type(ip)==str):
    new_ip=[]
    new_ip.append(ip)
    ip = new_ip



# Iniciar o subscritor
threading.Thread(target=subscriber_video, args=(ip_s)).start()
threading.Thread(target=subscriber_mensage, args=(ip_s)).start()
threading.Thread(target=subscriber_audio, args=(ip_s)).start()

# Iniciar o publicador

threading.Thread(target=publisher_video, args=(ip,)).start()
threading.Thread(target=publisher_mensage, args=(ip,nick)).start()
threading.Thread(target=publisher_audio, args=(ip,)).start()



# Aguardar o término do programa
while True:
    time.sleep(1)
