import os
import click
from spherical2images.utils_images import process_image
from spherical2images.utils import read_geojson, write_geojson


@click.command(short_help="Script to convert 360 images to simple sides images")
@click.option(
    "--input_images_folder",
    help="Input folder containing images",
    default="data/input_images",
)
@click.option(
    "--image_clip_size", help="Image size for each image to be clipped", default=1024
)
@click.option(
    "--output_images_path", help="Output images path", default="data",
)
@click.option(
    "--output_file_points",
    help="Output points for images that were processed",
    default="data/output_file_points.geojson",
)
@click.option(
    "--cube_sides", help="Sides of the image to save", default="right,left",
)
def main(
    input_images_folder,
    output_file_points,
    output_images_path,
    image_clip_size,
    cube_sides,
):

    image_files = [os.path.join(input_images_folder, f) for f in os.listdir(input_images_folder) if f.endswith((".jpg", ".JPG", ".jpeg", ".JPEG"))]
    output = process_image(image_files, output_images_path, image_clip_size, cube_sides)
    features = [fea for fea in output if fea is not None]
    write_geojson(output_file_points, features)


if __name__ == "__main__":
    main()
