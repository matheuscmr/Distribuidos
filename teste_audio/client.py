import zmq
import sounddevice as sd
import numpy as np

# Criação do contexto zmq
context = zmq.Context()

# Criação do socket zmq do tipo SUB (subscriber)
socket = context.socket(zmq.SUB)

# Conexão do socket ao endereço "tcp://localhost:5555"
socket.connect("tcp://localhost:5555")

# Configuração do socket para se inscrever em todos os tópicos
socket.subscribe("")

# Configuração do dispositivo de áudio
sample_rate = 44100
block_size = 1024

def audio_callback(indata, frames, time, status):
    # Função de callback de áudio vazia
    pass

def play_audio(data):
    # Converte os dados recebidos em um array numpy
    audio_data = np.frombuffer(data, dtype=np.float32)

    # Reproduz o áudio recebido
    sd.play(audio_data, samplerate=sample_rate, blocking=True)

# Criação do stream de entrada de áudio com as configurações definidas
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, blocksize=block_size)

# Inicia o streaming de áudio
stream.start()

# Aguarda a recepção e reprodução contínua do áudio
while True:
    # Recebe dados do socket
    data = socket.recv()

    # Reproduz o áudio recebido
    play_audio(data)
