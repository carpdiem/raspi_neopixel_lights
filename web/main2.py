from flask import Flask
from flask import request
import light_utilities2 as lu

strip = lu.initialize_strip()

app = Flask(__name__)

@app.route('/')
def index():
    return "index!"

@app.route('/lights_on', methods=['POST'])
def lights_on():
    if request.method == 'POST':
        color_temp = float(request.form['color_temp'])
        brightness = float(request.form['brightness'])
        lu.lights_on(strip, color_temp, brightness)

@app.route('/lights_off', methods=['POST'])
def lights_off():
    if request.method == 'POST':
        lu.lights_off(strip)

if __name__ == '__main__':
    app.run()
