from flask import Flask, render_template, Response
import cv2
# import RPi.GPIO as GPIO

app = Flask(__name__, template_folder='Client_Side')

#oude gsm voor camera
camera = cv2.VideoCapture('http://192.168.0.142:8080/video')

@app.route('/')
def home():
    return render_template('index.html')

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
    app.run(host='0.0.0.0')