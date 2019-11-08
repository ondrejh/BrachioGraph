#!/usr/bin/python3

from PIL import Image, ImageOps
from linedraw import makesvg, sortlines, hatch, getcontours, lines_to_file
import click


@click.command()
@click.option('--input', '-i', required=True)
@click.option('--output', '-o', required=True)
@click.option('--svg', '-s', default=None)
def click_app(input, output, svg):
    vector_it(image_filename=input, draw_hatch=False, output_filename=output, svg_filename=svg)


def vector_it(image_filename, resolution=1024, draw_hatch=True, hatch_size=16, draw_contours=True, contour_simplify=1,
              output_filename=None, svg_filename=None):

    image = Image.open(image_filename)
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
        f = open(svg_filename, 'w')
        f.write(makesvg(lines))
        f.close()

    segments = 0
    for line in lines:
        segments += len(line)

    print(len(lines), "strokes,", segments, "points.")
    print("done.")

    if output_filename is not None:
        lines_to_file(lines, output_filename)

    return lines


if __name__ == "__main__":

    click_app()
