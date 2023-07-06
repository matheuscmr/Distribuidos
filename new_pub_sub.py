import zmq
import time
import threading #biblioteca para criar threads e trabalhar em "paralelo"
import cv2 #biblioteca para transmitir video
import numpy as np
import pyaudio #biblioteca para transmitir audio


# A função subscriber_mensage, tem como objetivo se increver na porta para comunicação de texto 
# recebe como parametro ip_t, que é um conjunto de ips ao qual deseja se inscrever
def subscriber_mensagem(ip_t):
    # as 3 proximas linhas serao ações necessarias para realizar o conect
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    # o if a seguir fora feito para corrigir um bug, quando o codigo 
    # passava sem querer uma string ao inves de uma lista
    if (type(ip_t)==str):
        new_ip=[]
        new_ip.append(ip_t)
        ip_t = new_ip
    #aqui ele conectara em todos os ips passados
    for ip in ip_t:
        porta = "7000"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)
    #imprime as mensagens recebidas
    while True:
        message = socket.recv_string()
        print(message)
        

# A função subscriber_video, tem como objetivo se increver na porta para comunicação de video
# recebe como parametro ip_t, que é um conjunto de ips ao qual deseja se inscrever
def subscriber_video(ip_t):
    context = zmq.Context()
    sockets = []

    for ip in ip_t:
        porta = "7001"
        ip_complete = f"tcp://{ip}:{porta}"
        socket = context.socket(zmq.SUB)
        socket.setsockopt_string(zmq.SUBSCRIBE, '')
        socket.connect(ip_complete)
        sockets.append(socket)

    windows = {}  # Dicionário para mapear endereços IP para janelas do OpenCV

    while True:
        for i, socket in enumerate(sockets):
            frame_bytes = socket.recv()
            frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

            # Verificar se a janela correspondente ao endereço IP já existe
            if ip_t[i] not in windows:
                windows[ip_t[i]] = cv2.namedWindow(f"Recebendo video - {ip_t[i]}", cv2.WINDOW_NORMAL)

            cv2.imshow(f"Recebendo video - {ip_t[i]}", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


# A função subscriber_audio, tem como objetivo se increver na porta para comunicação de audio
# recebe como parametro ip_t, que é um conjunto de ips ao qual deseja se inscrever
def subscriber_audio(ip_t):
     # as 2 proximas linhas serao ações necessarias para realizar o connect
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    # o if a seguir fora feito para corrigir um bug, quando o codigo 
    # passava sem querer uma string ao inves de uma lista
    if (type(ip_t)==str):
        new_ip=[]
        new_ip.append(ip_t)
        ip_t = new_ip
    # aqui ele conectara em todos os ips passados
    for ip in ip_t:
        porta = "7002"
        ip_complete = f"tcp://{ip}:{porta}"
        socket.connect(ip_complete)
        socket.subscribe("")
    # configurando variaveis para receber o audio
    audio = pyaudio.PyAudio()
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    stream = audio.open(format=FORMAT,channels=CHANNELS,rate=RATE,output=True)

    while True:
            #recebimento e reprodução de audio
            audio_data = socket.recv()
            stream.write(audio_data)


# A função publisher_mensagem, tem como objetivo ser um publicador de conteudo em texto 
# recebe como um dos parametros ip, que é a a porta ao qual você dara bind (sua porta IPV4)
# recebe como um dos parametros o nick, que consiste no nick que ira aparecer do lado a sua mensagem enviada
def publisher_mensagem(ip,nick):
    # proximas 2 linhas coleta informações para realizar o bind
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    #porta que escolhemos para realizar o bind de mensagem
    porta = "7000"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)
    
    while True:
        # aqui ele anexa o nick a mensagem e envia para os subscribers
        message = input("Digite uma mensagem: ")
        message = f'{nick}: {message}'
        socket.send_string(message)


    

# A função publisher_video, tem como objetivo ser um publicador de conteudo em video
# recebe como um dos parametros ip, que é a a porta ao qual você dara bind (sua porta IPV4)
def publisher_video(ip):
    # proximas 2 linhas coleta informações para realizar o bind
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    #porta que escolhemos para realizar o bind de video
    porta = "7001"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)


    # inicia a captura de video
    video_capture = cv2.VideoCapture(0)

    while True:
        # realiza continuamente o envio de video
        ret, frame = video_capture.read()
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        socket.send(frame_bytes)



# A função publisher_audio, tem como objetivo ser um publicador de conteudo em audio
# recebe como um dos parametros ip, que é a a porta ao qual você dara bind (sua porta IPV4)
def publisher_audio(ip):
    # proximas 2 linhas coleta informações para realizar o bind
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    #porta que escolhemos para realizar o bind de audio
    porta = "7002"
    ip_complete = f"tcp://{ip}:{porta}"
    socket.bind(ip_complete)
    #da valores as variaveis necessarias para enviar o audio
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
        #realiza o envio de
        audio_data = stream.read(CHUNK)
        socket.send(audio_data)


#pega os dados a serem passados como parametro para as funções
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