from brachiograph import BrachioGraph as brachio
import click


@click.command()
@click.option('--input', '-i', required=True)
def draw(input):

    bg = brachio(8, 8, [-6, 5, 5, 13])
    bg.plot_file(input)

if __name__ == "__main__":

    draw()
