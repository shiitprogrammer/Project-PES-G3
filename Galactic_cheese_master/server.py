from flask import Flask, jsonify, render_template, request
import requests
import math
import Controller

app = Flask(__name__, template_folder='Client_Side')

def berekening_draaihoek(x, y, z, w):
    y = -y  
    z = -z  

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    radialen = math.atan2(t3, t4)

    graden = math.degrees(radialen)

    if graden < 0:
        graden += 360

    return graden

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rotation')
def get_rotation():
    url = 'http://192.168.0.142:8080/sensors.json'
    try:
        data = requests.get(url).json()
        rotation_vector = data['rot_vector']['data'][-1][1]
        x, y, z, w = rotation_vector[0:4]  # Extract quaternion components
        hoek_waarde = berekening_draaihoek(x, y, z, w)
        return jsonify({'hoek': hoek_waarde})
    except requests.RequestException as e:
        return jsonify({'fout': 'Failed to fetch data', 'details': str(e)}), 500
    except KeyError:
        return jsonify({'error': 'Malformed data received'}), 500



@app.route('/command/<cmd>', methods=['POST'])
@app.route('/command/<cmd>/<value>', methods=['POST'])
def handle_command(cmd, value=None):
    if cmd == 'shiet':
        Controller.shiet()
    elif cmd == 'dc_motor_snelheid':
        Controller.herladen()
    elif cmd == 'laser_toggle':
        Controller.laser_toggle()
    elif cmd == 'draai_links':
        Controller.draai_links(value)
    elif cmd == 'draai_rechts':
        Controller.draai_rechts(value)
    return ({'status': 'success', 'cmd': cmd, 'value': value})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
