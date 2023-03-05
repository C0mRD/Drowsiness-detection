from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
import cv2
import numpy as np
from model import *

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, ping_interval=10, ping_timeout=120)


@socketio.on('frame')
def process_frame(frame):
    # Convert data URL to OpenCV image
    data = frame.split(',')[1]
    data = bytes(data, 'utf-8')
    data = base64.b64decode(data)

    img = cv2.imdecode(np.fromstring(data, np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img, (640, 480))

    # Process the image
    img = process_frames(img)

    # Encode the processed image as JPEG and send it to the client
    _, buffer = cv2.imencode('.jpg', img)
    data = base64.b64encode(buffer)
    data = data.decode('utf-8')
    emit('image', data)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
