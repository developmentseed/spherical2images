import requests
import json
import os
import click
from joblib import Parallel, delayed
from tqdm import tqdm
from cubemap_splitter import split_cubemap
import os
from pathlib import Path
import glob
from smart_open import open


access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")


def download_process_img(feature, output_images_path, image_clip_size):
    """Download and clip the spherical image

    Args:
        feature (dict): feture
        output_images_path (str): path to save the images
        image_clip_size (int): Size of the image to clip
    Returns:
        [dict]: feature
    """
    sequence_id = feature["properties"]["sequence_id"]
    image_folder_path = f"{output_images_path}/{sequence_id}"
    new_feature = None
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)

    # request the URL of each image
    image_id = feature["properties"]["id"]

    # Check if mapillary image exist and download
    img_file_equirectangular = f"{image_folder_path}/{image_id}.jpg"
    img_file_cubemap = f"{image_folder_path}/{image_id}_cubemap.jpg"

    if not os.path.isfile(img_file_equirectangular):
        header = {"Authorization": "OAuth {}".format(access_token)}
        url = "https://graph.mapillary.com/{}?fields=thumb_2048_url".format(image_id)

        try:
            r = requests.get(url, headers=header)
            data = r.json()
            image_url = data["thumb_2048_url"]
            with open(img_file_equirectangular, "wb") as handler:
                image_data = requests.get(image_url, stream=True).content
                handler.write(image_data)

            # Convert Equirectangular -> Cubemap
            cmd = f"convert360 --convert e2c --i {img_file_equirectangular}  --o {img_file_cubemap} --w {image_clip_size}"
            os.system(cmd)

            # Split Cubemap to simple images
            chumk_image_path = f"{image_folder_path}/{image_id}"
            if not os.path.exists(chumk_image_path):
                os.makedirs(chumk_image_path)
            split_cubemap(img_file_cubemap, format_type=1, output_directory=chumk_image_path)
            # Rename files
            clean_files(image_folder_path, image_id)
            new_feature = feature
        except requests.exceptions.HTTPError as err:
            print(err)
        except OSError as err:
            print(err)
        except KeyError as err:
            print(err)
    else:
        print(f"File exist..{img_file_equirectangular}")

    return new_feature


def clean_files(image_folder_path, image_id):
    chumk_image_path = f"{image_folder_path}/{image_id}"
    for file in glob.glob(f"{chumk_image_path}/*.jpg"):
        side = Path(file).stem
        os.rename(
            f"{chumk_image_path}/{side}.jpg",
            f"{image_folder_path}/{image_id}_{side}.jpg",
        )


def process_image(input_points, output_images_path, image_clip_size):

    with open(input_points, "r", encoding="utf8") as f:
        features = json.load(f)["features"]

    # Process in parallel
    results = Parallel(n_jobs=-1)(
        delayed(download_process_img)(feature, output_images_path, image_clip_size)
        for feature in tqdm(features, desc=f"Processing images for...", total=len(features))
    )
    return features


@click.command(short_help="Script to conver 360 images to simple sides images")
@click.option(
    "--input_points",
    help="input points geojson file",
    default="data/input_points.geojson",
)
@click.option("--image_clip_size", help="Image size of the image to clip", default=1024)
@click.option(
    "--output_images_path",
    help="Output images path",
    default="data",
)
@click.option(
    "--output_points",
    help="output points for images that were processed",
    default="data/output_points.geojson",
)
def main(input_points, output_points, output_images_path, image_clip_size):
    output = process_image(input_points, output_images_path, image_clip_size)
    features = [fea for fea in output if fea is not None]
    with open(output_points, "w") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)


if __name__ == "__main__":
    main()
