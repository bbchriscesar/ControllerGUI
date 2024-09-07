import time
import serial
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BAUD_RATE = 9600


def send_command(port, command):
    try:
        with serial.Serial(port, BAUD_RATE, timeout=1) as ser:
            time.sleep(2)
            ser.write(command.encode())
            time.sleep(0.5)
        return f"Sent command: {command} to port: {port}"
    except serial.SerialException as e:
        return f"Error: {str(e)}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rotate', methods=['POST'])
def rotate():
    data = request.json
    port = data['port']
    direction = data['direction']
    if direction in ['f', 'b']:
        result = send_command(port, direction)
        return jsonify({"message": result})
    else:
        return jsonify({"message": "Invalid command. Please use 'f' or 'b'."}), 400


if __name__ == '__main__':
    app.run(debug=True)
