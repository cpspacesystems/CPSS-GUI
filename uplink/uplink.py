#!/usr/bin/python
# coding: utf-8
from flask import Flask, render_template, request, jsonify
# from util import get_cfg
import serial
import serial.tools.list_ports

RATE = 57600
ports = [p.device for p in serial.tools.list_ports.comports()]

form = {'action_A': False,
        'action_B': False,
        'action_C': False,
        'action_D': False,
        'action_E': False,
        'action_F': False,
        'action_G': False,
        'action_G': False,
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

        if(form['port']):
            if('A' in request.form):
                form['action_A'] = not form['action_A']
                msg = "ACTION_A_ABC\n"
                
            if('B' in request.form):
                form['action_B'] = not form['action_B']
                msg = "ACTION_B_DEF\n"

            if('C' in request.form):
                form['action_C'] = not form['action_C']
                msg = "ACTION_C_GHI\n"

            if('D' in request.form):
                form['action_D'] = not form['action_D']
                msg = "ACTION_D_JKL\n"

            if('E' in request.form):
                form['action_E'] = not form['action_E']
                msg = "ACTION_E_MNO\n"

            if('F' in request.form):
                form['action_F'] = not form['action_F']
                msg = "ACTION_F_PQR\n"
            
            if('G' in request.form):
                form['action_G'] = not form['action_G']
                msg = "ACTION_G_STU\n"
            
            if('H' in request.form):
                form['action_H'] = not form['action_H']
                msg = "ACTION_H_VWX\n"

    if(msg and form['port']):
        print(msg)
        with serial.Serial(form['port'], RATE, timeout=1) as ser:
            ser.write(msg.encode())

    return render_template('dashboard.html', form=form)

def start():
    app.run()

if __name__ == '__main__':
    app.run(debug=True)
