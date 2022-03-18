import requests
import json
import os
import click
from joblib import Parallel, delayed
from tqdm import tqdm
import os
from pathlib import Path
import glob
from smart_open import open
from spherical2images.utils_images import process_image


@click.command(short_help="Script to convert 360 images to simple sides images")
@click.option(
    "--input_file_points",
    help="Input geojson file of points",
    default="data/input_file_points.geojson",
)
@click.option(
    "--image_clip_size", help="Image size for each image to be clipped", default=1024
)
@click.option(
    "--output_images_path",
    help="Output images path",
    default="data",
)
@click.option(
    "--output_file_points",
    help="Output points for images that were processed",
    default="data/output_file_points.geojson",
)
@click.option(
    "--cube_sides",
    help="Sides of the image to save",
    default="right,left",
)
def main(
    input_file_points,
    output_file_points,
    output_images_path,
    image_clip_size,
    cube_sides,
):
    output = process_image(
        input_file_points, output_images_path, image_clip_size, cube_sides
    )
    features = [fea for fea in output if fea is not None]
    with open(output_file_points, "w") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)


if __name__ == "__main__":
    main()
