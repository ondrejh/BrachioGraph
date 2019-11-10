#!/usr/bin/python3

from flask import Flask, render_template, send_file
import os
import glob

#dir = '/home/pi/brachio/templates/img/'
#if not os.path.isdir(dir):
dir = 'templates/img/'

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
        fn = os.path.abspath(os.path.join(dir, filename))
        bg.draw(fn)
    images = glob.glob(os.path.join(dir, '*.svg'))
    print(images)
    return render_template('index.html')


@webi.route('/favicon.ico')
def favicon():
    return send_file('templates/favicon.ico')


@webi.route('/style.css')
def style():
    return send_file('templates/style.css')


@webi.route('/img/<name>')
def image(name):
    return send_file('templates/img/{}'.format(name))


if __name__ == "__main__":
    bg.start()
    webi.run(host='0.0.0.0')
    bg.stop()