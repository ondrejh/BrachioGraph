#!/usr/bin/python3

from brachiograph import BrachioGraph as brachio
import threading
from time import sleep
import os

INNER_ARM_DEFAULT = 8
OUTER_ARM_DEFAULT = 8
BOUNDS_DEFAULT = [-6, 5, 5, 13]


class BrachioThread(threading.Thread):

    def __init__(self, inner=INNER_ARM_DEFAULT, outer=OUTER_ARM_DEFAULT, bounds=BOUNDS_DEFAULT):
        threading.Thread.__init__(self)
        self.inner = inner
        self.outer = outer
        self.bounds = bounds

        self.brachio = None

        self.busy = True

    def stop(self):

        self.brachio.quiet()
        self.brachio = None

    def quiet(self):

        if (self.brachio is not None) and (not self.busy):
            self.busy = True
            self.brachio.quiet()
            self.busy = False

    def park(self):

        if (self.brachio is not None) and (not self.busy):
            self.busy = True
            self.brachio.park()
            self.busy = False

    def draw(self, filename):

        if (os.path.isfile(filename)) and (self.brachio is not None) and (not self.busy):
            self.busy = True
            try:
                self.brachio.plot_file(filename)
            except KeyboardInterrupt:
                pass
            self.busy = False

    def box(self):

        if (self.brachio is not None) and (not self.busy):
            self.busy = True
            self.brachio.box()
            self.busy = False

    def run(self):

        self.brachio = brachio(self.inner, self.outer, self.bounds)
        self.busy = False

        while self.brachio is not None:

            sleep(0.5)


if __name__ == "__main__":

    bg = BrachioThread()
    bg.start()

    print()
    sleep(3)
    print('park')
    bg.park()

    sleep(3)
    print('box ', end='')
    bg.box()

    while bg.busy:
        sleep(1)
        print('.', end='')
    print()

    sleep(1)
    bg.park()
    print('park')
    sleep(1)
    bg.quiet()
    print('quiet')
    sleep(1)
    bg.stop()
    sleep(1)
    print('finito ...')
