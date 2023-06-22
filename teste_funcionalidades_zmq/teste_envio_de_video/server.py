import zmq
import cv2

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    # Serialize o quadro como uma sequência de bytes
    frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

    # Envia o quadro para os clientes inscritos
    socket.send(frame_bytes)