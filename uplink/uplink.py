#!/usr/bin/python
# coding: utf-8
from flask import Flask, render_template, request, jsonify
# from util import get_cfg
import serial

form = {'state' : 'STATE_1',
        'nose_cone' : 0,
        'action_A': False,
        'action_B': False}

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def entry_point():
    if request.method == 'POST':
        if('state' in request.form):
            form['state'] = request.form['state']
        if('nose_cone' in request.form):
            form['nose_cone'] = request.form['nose_cone']
        if('action_A' in request.form):
            form['action_A'] = not form['action_A']
        if('action_B' in request.form):
            form['action_B'] = not form['action_B']
    # print(request.form)
    return render_template('index.html', form=form)

def start():
    app.run()

if __name__ == '__main__':
    # cfg = get_cfg()
    app.run(debug=True)

