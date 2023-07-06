import zmq
import sounddevice as sd
import numpy as np

# Criação do contexto zmq
context = zmq.Context()

# Criação do socket zmq do tipo PUB (publisher)
socket = context.socket(zmq.PUB)

# Faz o bind do socket ao endereço "tcp://*:5555"
socket.bind("tcp://*:5555")

# Configuração do dispositivo de áudio
sample_rate = 44100
block_size = 1024

def audio_callback(indata, frames, time, status):
    # Envia os blocos de áudio para os clientes inscritos
    socket.send(indata.tobytes())

# Criação do stream de entrada de áudio com as configurações definidas
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, blocksize=block_size)

# Inicia o streaming de áudio
stream.start()

# Aguarda a finalização da transmissão
while True:
    # Loop vazio, aguardando indefinidamente
    pass
