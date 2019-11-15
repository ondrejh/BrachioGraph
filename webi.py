#!/usr/bin/python3

from flask import Flask, render_template, send_file
import os
import glob

dir = 'templates/img/'

webi = Flask(__name__)
bg = None
ptr = 0

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
def index(command=None):
    images = glob.glob(os.path.join(dir, '*.svg'))
    #print(images)
    ptr_max = len(images) - 1
    global ptr
    if command is not None:
        if command == 'park':
            bg.park()
        elif command == 'box':
            bg.box()
        elif command == 'quiet':
            bg.quiet()
        elif command == 'next':
            if ptr < ptr_max:
                ptr += 1
        elif command == 'prev':
            if ptr > 0:
                ptr -= 1
        elif command == 'draw':
            fn = os.path.abspath(os.path.splitext(images[ptr])[0]+'.json')
            bg.draw(fn)
    return render_template('index.html', image=os.path.join('img', os.path.basename(images[ptr])),
                           cnt=ptr, cnt_of=ptr_max)


@webi.route('/favicon.ico')
def favicon():
    return send_file('templates/favicon.ico')


@webi.route('/<name>.css')
def style(name=None):
    fpath = 'templates/{}.css'.format(name)
    if os.path.isfile(fpath):
        return send_file(fpath)


@webi.route('/<name>.js')
def js(name=None):
    fpath = 'templates/{}.js'.format(name)
    if os.path.isfile(fpath):
        return send_file(fpath)


@webi.route('/img/<name>')
def image(name):
    return send_file('templates/img/{}'.format(name))


@webi.route('/images/<name>')
def image_lb(name):
    return send_file('templates/img/{}'.format(name))


if __name__ == "__main__":
    bg.start()
    webi.run(host='0.0.0.0')
    bg.stop()