#!/usr/bin/python3

import click
from brachiograph import BrachioGraph as brachio


@click.command()
@click.option('--input', '-i', required=True)
def draw(input):

    bg = brachio(8, 8, [-6, 5, 5, 13])
    try:
        bg.plot_file(filename=input)
    except KeyboardInterrupt:
        bg.park()

if __name__ == "__main__":

    draw()
