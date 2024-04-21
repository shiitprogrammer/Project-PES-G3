from flask import Flask, render_template, Response, url_for, jsonify
import cv2
import time
import os
import numpy as np
from datetime import datetime

app = Flask(__name__, template_folder='Client_Side')

# Oude GSM voor camera
camera = cv2.VideoCapture('http://192.168.137.142:8080/video')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/instellingen')
def instellingen():
    return render_template('instellingen.html')

def generate_frames():
    while True:
        success, frame = camera.read()
        if success:
            if frame.shape[0] > frame.shape[1]:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            print("niet gelukt, Opnieuw verbinden..")
            opnieuw_verbinden()

def opnieuw_verbinden():
    global camera
    camera.release()
    time.sleep(2) 
    camera = cv2.VideoCapture('http://192.168.0.142:8080/video')
    if camera.isOpened():
        print("opnieuw verbonden!")
    else:
        print("weer mislukt. Opnieuw proberen...")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/analyze')
def analyze_with_angles(image_path=None):
    for _ in range(10):  
        camera.grab()
    success, frame = camera.read()
    if success:
        if frame.shape[0] > frame.shape[1]:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        static_path = os.path.join(app.root_path, 'static')
        if not os.path.exists(static_path):
            os.makedirs(static_path)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f'processed_image_{timestamp}.jpg'
        save_path = os.path.join(static_path, filename)
        cv2.imwrite(save_path, frame)

        image_url = url_for('static', filename=filename)
        return jsonify({'image_url': image_url})

    else:
        return jsonify({'error': 'Unable to capture image'}), 500



@app.route('/command/<cmd>', methods=['POST'])
@app.route('/command/<cmd>/<value>', methods=['POST'])
def handle_command(cmd, value=None):
    if cmd == 'draai_links':
        print('Links draaien')
        return 'linksdraaien'
    elif cmd == 'draai_rechts':
        print('Rechts draaien')
        return 'rechtsdraaien'
    elif cmd == 'schiet':
        print('Schieten')
        return 'geschoten'
    elif cmd == 'herlaad':
        print('Herladen')
        return 'herladen'
    elif cmd == 'stop':
        print('Stop')
        return 'gestopt'
    elif cmd == 'updateMotorPower':
        print(f'Update motor power naar {value}')
        
        return 'Motor power updated'
    else:
        return 'Geen commando', 400


    
if __name__ == '__main__':
    app.run()
