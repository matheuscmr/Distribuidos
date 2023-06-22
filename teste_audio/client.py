import zmq
import sounddevice as sd
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.subscribe("")

# Configuração do dispositivo de áudio
sample_rate = 44100
block_size = 1024

def audio_callback(indata, frames, time, status):
    pass

def play_audio(data):
    # Converte os dados recebidos em um array numpy
    audio_data = np.frombuffer(data, dtype=np.float32)

    # Reproduz o áudio recebido
    sd.play(audio_data, samplerate=sample_rate, blocking=True)

stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, blocksize=block_size)
stream.start()

# Aguarda a recepção e reprodução contínua do áudio
while True:
    data = socket.recv()
    play_audio(data)
