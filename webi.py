#!/usr/bin/python3

from flask import Flask, render_template, send_file
import os

dir = '/home/pi/brachio/templates/img/'

webi = Flask(__name__)
bg = None

try:
    from brachio_thread import BrachioThread
    bg = BrachioThread()
except ImportError:
    class BrachioTestClass():
        def park(self):
            print('park')
        def box(self):
            print('box')
        def quiet(self):
            print('quiet')
        def start(self):
            print('start')
        def stop(self):
            print('stop')
        def draw(self, filename):
            print('draw {}'.format(filename))
    bg = BrachioTestClass()


@webi.route('/')
@webi.route('/cmd=<command>')
@webi.route('/draw=<filename>')
def index(command=None,filename=None):
    if command is not None:
        if command == 'park':
            bg.park()
        elif command == 'box':
            bg.box()
        elif command == 'quiet':
            bg.quiet()
    if filename is not None:
        fn = os.path.join(dir, filename)
        bg.draw(fn)
    return render_template('index.html')

@webi.route('/favicon.ico')
def favicon():
    return send_file('templates/favicon.ico')

if __name__ == "__main__":
    bg.start()
    webi.run(host='0.0.0.0')
    bg.stop()