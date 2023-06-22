import zmq
import sounddevice as sd
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

# Configuração do dispositivo de áudio
sample_rate = 44100
block_size = 1024

def audio_callback(indata, frames, time, status):
    # Envia os blocos de áudio para os clientes inscritos
    socket.send(indata.tobytes())

stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, blocksize=block_size)
stream.start()

# Aguarda a finalização da transmissão
while True:
    pass