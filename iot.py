from flask import Flask,stream_with_context, request, Response,jsonify


app = Flask(__name__)


import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = '/sys/bus/w1/devices/28-0416b358d0ff/w1_slave'


def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()

    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return str(temp_f)


@app.route('/')
def stream():
    def generate():
        while True:
            yield "{'temperature':"+read_temp()+"}"
            time.sleep(1)
    return Response(stream_with_context(generate()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
