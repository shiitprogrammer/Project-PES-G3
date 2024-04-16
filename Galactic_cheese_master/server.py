from flask import Flask, render_template
# import RPi.GPIO as GPIO

app = Flask(__name__, template_folder='Client_Side')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/command/<cmd>', methods=['POST'])
def handle_command(cmd):
    if cmd == 'draai_links':
        # code om de robot links te draaien
        return 'linksdraaien'
    elif cmd == 'draai_rechts':
        # Code om de robot rechts te draaien
        return 'rechtsdraaien'
    elif cmd == 'schiet':
        # Code om te schieten
        return 'geschoten'
    elif cmd == 'herlaad':
        # Code om te herladen
        return 'herladen'
    else:
        return 'Geen commando', 400

if __name__ == '__main__':
    app.run()