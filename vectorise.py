#!/usr/bin/python3

from PIL import Image, ImageOps
from linedraw import makesvg, sortlines, hatch, getcontours, lines_to_file
import click
import os


@click.command()
@click.option('--input', '-i', required=True)
@click.option('--output', '-o', required=True)
@click.option('--svg', '-s', default=None)
@click.option('--dir', '-d', default=None)
def click_app(input, output, svg, dir):
    vector_it(image_filename=input, draw_hatch=False, output_filename=output, svg_filename=svg, work_dir=dir)


def vector_it(image_filename, resolution=1024, draw_hatch=True, hatch_size=16, draw_contours=True, contour_simplify=2,
              output_filename=None, svg_filename=None, work_dir=None):

    ifn = image_filename
    if work_dir is not None:
        ifn = os.path.join(work_dir, image_filename)
    image = Image.open(ifn)
    w, h = image.size

    # convert the image to grey scale
    image = image.convert("L")

    # maximise contrast
    image = ImageOps.autocontrast(image, 10)

    lines = []

    if draw_contours:
        lines += sortlines(getcontours(
            image.resize((int(resolution/contour_simplify), int(resolution/contour_simplify*h/w))),
            contour_simplify,
        ))

    if draw_hatch:
        lines += sortlines(
            hatch(
                # image,
                image.resize((int(resolution/hatch_size), int(resolution/hatch_size*h/w))),
                hatch_size,
            )
        )

    if svg_filename is not None:
        sfn = svg_filename
        if work_dir:
            sfn = os.path.join(work_dir, svg_filename)
        f = open(sfn, 'w')
        f.write(makesvg(lines))
        f.close()

    segments = 0
    for line in lines:
        segments += len(line)

    print(len(lines), "strokes,", segments, "points.")
    print("done.")

    if output_filename is not None:
        ofn = output_filename
        if work_dir:
            ofn = os.path.join(work_dir, output_filename)
        lines_to_file(lines, ofn)

    return lines


if __name__ == "__main__":

    click_app()
