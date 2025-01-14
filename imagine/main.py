from pathlib import Path
import click
from PIL import Image


@click.group(chain=True)
def cli():
    """Imagine provides tools to resize, edit, transform, create images and thumbnails and convert between file formats"""
    pass


@cli.command()
@click.argument("image", type=click.Path(exists=True, file_okay=True))
@click.option("--s", is_flag=True, default=False, help="display size of image")
@click.option("--m", is_flag=True, default=False, help="display mode of image")
@click.option("--f", is_flag=True, default=False, help="display format of image")
def image_info(image, s, m, f):
    """
    Show the information related to the image file.

    Information includes\n
        - format: identifies the source of the image. Set to none if the image was not read from a file.\n
        - size: the width and height (in pixels) respectively\n
        - mode: defines the number, names, pixel type and depth of the channels in the image. Modes include 'Luminance', 'RGB' and 'CMYK'
    """

    im = Image.open(image)
    img_format, img_size, img_mode = (im.format, im.size, im.mode)
    if s:
        click.echo(f"Width: {img_size[0]} Height: {img_size[1]}")
    if m:
        click.echo(f"Mode: {im.mode}")
    if f:
        click.echo(f"Format: {im.format}")
    if not s and not m and not f:
        click.echo(f"format: {img_format}, size: {img_size} mode: {img_mode}")


@cli.command()
@click.argument("image", type=click.Path(exists=True, file_okay=True))
def process_image(image):
    """Process a single image in the provided directory

    eg: imagine process_image /home/nimo/Desktop/pictures/ball.png
    """
    im = Image.open(image)
    img_format, img_size, img_mode = (im.format, im.size, im.mode)

    click.echo(f"format: {img_format}, size: {img_size} mode: {img_mode}")


@cli.command()
@click.argument("directory", type=click.Path(exists=True, dir_okay=True))
@click.option(
    "--r",
    is_flag=True,
    show_default=True,
    default=False,
    help="Recursively show images shows in subdirectories of specified directory",
)
def show_images(directory, r):
    """Show images in the specified directory

    eg: imagine show-images /home/nimo/Desktop/pictures/
    """
    new_path = Path(directory)

    if r:
        files = new_path.rglob("*.png")
        for f in files:
            click.echo(f.name)
        print("done==========")
    else:
        for path in new_path.iterdir():
            if not path.is_dir():
                click.echo(path.name)
    # 4. Check if the files are of image types and print them out or throw error
