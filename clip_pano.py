import mercantile
from numpy import integer
import requests
import json
import os
import click
from joblib import Parallel, delayed
from tqdm import tqdm
from vt2geojson.tools import vt_bytes_to_geojson

access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")
sides_dict = {
    "0": "front",
    "1": "left",
    "2": "right",
    "3": "back",
    "4": "over",
    "5": "under",
}


def download_process_img(feature, output_images_path, image_clip_size, cube_sides):
    """Download and clip the spherical image

    Args:
        feature (dict): feture
        output_images_path (str): path to save the images
        image_clip_size (int): Size of the image to clip
        cube_sides (str): list of sited to clip

    Returns:
        [dict]: feature
    """
    sequence_id = feature["properties"]["sequence_id"]
    image_folder_path = f"{output_images_path}/{sequence_id}"
    print(image_folder_path)

    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)

    # request the URL of each image
    image_id = feature["properties"]["id"]

    # Check if mapillary image exist and download
    img_file = f"{image_folder_path}/{image_id}.jpg"
    if not os.path.isfile(img_file):
        header = {"Authorization": "OAuth {}".format(access_token)}
        url = "https://graph.mapillary.com/{}?fields=thumb_2048_url".format(
            image_id)
        r = requests.get(url, headers=header)
        data = r.json()
        image_url = data["thumb_2048_url"]
        with open(img_file, "wb") as handler:
            image_data = requests.get(image_url, stream=True).content
            handler.write(image_data)
    else:
        print(f"File exist..{img_file}")

    # Check if chuck files exist
    list_sides = []
    cube_list = cube_sides.split(",")
    for i in cube_list:
        if i in sides_dict.keys():
            img_cube_chunk = f"{image_folder_path}/{image_id}_{sides_dict[i]}.jpg"
            if not os.path.isfile(img_cube_chunk):
                list_sides.append(i)
            else:
                print(f"File exist..{img_cube_chunk}")

    # Split spherical image into chunks
    if len(list_sides) > 0:
        str_sides = ",".join(list_sides)
        os.system(
            f"sphericalpano2cube -d {image_clip_size} -s {cube_sides} {img_file} {img_file}")
    # TODO Upload to cloud provider
    return feature


def process_image(input_points, output_images_path, image_clip_size, cube_sides):

    with open(input_points, "r", encoding="utf8") as f:
        features = json.load(f)["features"]

    # Process in parallel
    results = Parallel(n_jobs=-1)(
        delayed(download_process_img)(
            feature, output_images_path, image_clip_size,  cube_sides)
        for feature in tqdm(features, desc=f"Processing images for...", total=len(features))
    )
    return features


@click.command(short_help="Script to get last updates for adapters")
@click.option(
    "--input_points",
    help="input points geojson file",
    default="data/input_points.geojson",
)
@click.option(
    "--cube_sides",
    help="""Select which sides  need to be extracted: 
        - 0:front
		- 1:left
		- 2:right
		- 3:back
		- 4:over
		- 5:under""",
    default="1,2",
    type=str,
)
@click.option(
    "--image_clip_size",
    help="Image size of the image to clip",
    default=512
)
@click.option(
    "--output_images_path",
    help="Output images path",
    default="data/images",
)
@click.option(
    "--output_points",
    help="output points for images that were processed",
    default="data/output_points.geojson",
)
def main(input_points, output_points, output_images_path, image_clip_size, cube_sides):
    output = process_image(input_points, output_images_path,
                           image_clip_size, cube_sides)
    with open(output_points, "w") as f:
        json.dump({"type": "FeatureCollection", "features": output}, f)


if __name__ == "__main__":
    main()
