from pathlib import Path
import click

# from click_extra import extra_command
from click_extra import extra_group, extra_command
from PIL import Image, ImageOps


IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".jpe",
    ".jif",
    ".jfif",
    ".jfi",
    ".gif",
    ".webp",
    ".tiff",
    ".tif",
    ".svg",
    ".svgz",
    ".heif",
    ".heic",
    ".bmp",
    ".dib",
}

COLORS: dict[str, str] = {
    "success": "green",
    "failed": "red",
}


@click.group(chain=True)
@click.pass_context
def cli(ctx):
    """Imagine provides tools to resize, edit, transform, create images and thumbnails and convert between file formats"""
    ctx.ensure_object(dict)

    # set the working directory where all operations should take place
    ctx.obj["working_dir"] = "None"


# TODO: Still under development
@cli.command()
@click.pass_context
@click.argument("working_directory", type=click.Path(exists=True, dir_okay=True))
def set_working_dir(ctx, working_directory):
    """
    Set the working directory for IMAGINE to look for all images.
    If specified, commands requiring directories can be run without specifying
    """

    specified_dir = Path(working_directory)

    # check to see if there is at least one image in the specified directory
    try:
        count: int = 0
        for ext in IMAGE_EXTENSIONS:
            files = specified_dir.rglob(f"*{ext}")

            for file in files:
                if file.suffix in IMAGE_EXTENSIONS:
                    count += 1  # there is a supported image format in directory

        if count > 0:
            click.echo(f"{count} Supported Image format(s) found")
            ctx.obj.update({"working_dir": working_directory})

            click.secho(f"working directory: {working_directory}", fg=COLORS["success"])

            click.echo(ctx.obj["working_dir"])

        else:
            raise click.ClickException(
                message="Supported image(s) format not found in directory"
            )

    except click.ClickException as e:
        click.secho(e.message, fg=COLORS["failed"])


@cli.command()
@click.argument(
    "image",
    type=click.Path(exists=True, file_okay=True),
)
@click.option("--s", is_flag=True, default=False, help="display size of image")
@click.option("--m", is_flag=True, default=False, help="display mode of image")
@click.option("--f", is_flag=True, default=False, help="display format of image")
@click.pass_context
def image_info(ctx, image, s, m, f):
    """
    Show the information related to the image file.

    Information includes\n
        - format: identifies the source of the image. Set to none if the image was not read from a file.\n
        - size: the width and height (in pixels) respectively\n
        - mode: defines the number, names, pixel type and depth of the channels in the image. Modes include 'Luminance', 'RGB' and 'CMYK'
    """

    # image = "/home/nova/Desktop/projects/imagine/images/j-image-3.jpeg"
    click.secho(ctx.obj["working_dir"], fg=COLORS["success"])

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
@click.option("--save-to", "-s")
def process_image(image, save_to, help="directory to save proccessed image to"):
    """Process a single image in the provided directory\n
    Process image is automatically saved in the same directory unless specified

    eg: imagine process_image /home/nimo/Desktop/pictures/ball.png
    """
    im = Image.open(image)
    img_format, img_size, img_mode = (im.format, im.size, im.mode)

    # Process image directory to return only directory path
    current_image_path = image.split("/")
    new_folder_path = current_image_path[0:-1]
    image_folder = "/".join(new_folder_path) + "/"

    click.echo("IMAGE INFO")
    click.echo(f"format: {img_format}, size: {img_size} mode: {img_mode}")
    click.echo(f"Folder: {image_folder}")
    click.echo("\n*** Image opened for processing ***")
    click.echo("*** Select from the options below to continue ***")
    click.echo("1.Resize Image\n2.Convert to other image formats")

    user_choice: int = click.prompt(">> ", type=int)
    new_filename: str = ""

    try:
        if user_choice < 1:
            raise click.ClickException("Enter a valid option")

        # check if the user_choice is resize
        if user_choice == 1:
            # prompt user to enter the width and height respectively
            width: int = click.prompt("Width >> ", type=int)
            height: int = click.prompt("Height >> ", type=int)

            ans: bool = click.confirm("Use Default file name? >>", default=True)
            if ans:
                new_filename = image.split("/")[-1]
            else:
                user_input = click.prompt("Enter new file name", type=str)
                new_filename = user_input + "." + image.split("/")[-1].split(".")[-1]
                click.echo(f"new file name is: {new_filename}")

            size = (width, height)

            with Image.open(image) as editable_img:
                ImageOps.contain(editable_img, size).save(
                    f"{image_folder}/{new_filename}"
                )

    except click.ClickException as e:
        click.secho(e, fg=COLORS["failed"])


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
        for ext in IMAGE_EXTENSIONS:
            files = new_path.rglob(f"*{ext}")
            for file in files:
                if file.suffix in IMAGE_EXTENSIONS:
                    click.echo(file.name)
    else:
        for path in new_path.iterdir():
            if not path.is_dir():
                click.echo(path.name)
