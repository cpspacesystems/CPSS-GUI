#!/usr/bin/python
# coding: utf-8
from flask import Flask, render_template, request, jsonify
# from util import get_cfg
import serial
import serial.tools.list_ports

RATE = 57600
ports = [p.device for p in serial.tools.list_ports.comports()]

form = {'state' : 'STATE_1',
        'nose_cone' : 0,
        'action_A': False,
        'action_B': False,
        'ports' : ports,
        'port': ""}

app = Flask(__name__)

# TODO: get confirmation packets so we know the function was executed
@app.route('/', methods=('GET', 'POST'))
def entry_point():
    msg = ""
    if request.method == 'POST':
            if('port' in request.form):
                form['port'] = request.form['port']
            if('state' in request.form):
                form['state'] = request.form['state']
                # msg = "STATE={}\n".format(form['state'])
                msg = "funcA\n"
            if('nose_cone' in request.form):
                form['nose_cone'] = request.form['nose_cone']
                msg = "NOSE_CONE={}\n".format(form['nose_cone'])
            if('action_A' in request.form):
                form['action_A'] = not form['action_A']
                msg = "ACTION_A\n"
            if('action_B' in request.form):
                form['action_B'] = not form['action_B']
                msg = "ACTION_B\n"

    if(msg and form['port']):
        with serial.Serial(form['port'], RATE, timeout=1) as ser:
            ser.write(msg.encode())

    # print(request.form)
    return render_template('dashboard.html', form=form)

def start():
    app.run()

if __name__ == '__main__':
    app.run(debug=True)
