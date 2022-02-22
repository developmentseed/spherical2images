from numpy import integer
import requests
import json
import os
import click
from joblib import Parallel, delayed
from tqdm import tqdm
from cubemap_splitter import split_cubemap
import os
from pathlib import Path
import shutil
import glob

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

    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)

    # request the URL of each image
    image_id = feature["properties"]["id"]

    # Check if mapillary image exist and download
    img_file_equirectangular = f"{image_folder_path}/{image_id}.jpg"
    img_file_cubemap = f"{image_folder_path}/{image_id}_cubemap.jpg"

    if not os.path.isfile(img_file_equirectangular):
        header = {"Authorization": "OAuth {}".format(access_token)}
        url = "https://graph.mapillary.com/{}?fields=thumb_2048_url".format(
            image_id)

        try:
            r = requests.get(url, headers=header)
            data = r.json()
            image_url = data["thumb_2048_url"]
            with open(img_file_equirectangular, "wb") as handler:
                image_data = requests.get(image_url, stream=True).content
                handler.write(image_data)

            # Convert Equirectangular -> Cubemap
            cmd =f"convert360 --convert e2c --i {img_file_equirectangular}  --o {img_file_cubemap} --w {image_clip_size}"
            os.system(cmd)

            # Split Cubemap to simple images
            chumk_image_path = f"{image_folder_path}/{image_id}"
            if not os.path.exists(chumk_image_path):
                os.makedirs(chumk_image_path)
            split_cubemap(img_file_cubemap, format_type=1,
                          output_directory=chumk_image_path)
            # Rename files
            clean_files(image_folder_path, image_id)

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except OSError as error : 
            print(error)

    else:
        print(f"File exist..{img_file_equirectangular}")

    # # Check if chuck image files exist
    # list_sides = []
    # cube_list = cube_sides.split(",")
    # for i in cube_list:
    #     if i in sides_dict.keys():
    #         img_cube_chunk = f"{image_folder_path}/{image_id}_{sides_dict[i]}.jpg"
    #         if not os.path.isfile(img_cube_chunk):
    #             list_sides.append(i)
    #         else:
    #             print(f"File exist..{img_cube_chunk}")

    # # Split spherical image into chunks
    # if len(list_sides) > 0:
    #     # Convert Equirectangular -> Cubemap
    #     os.system(
    #         f"convert360 --convert e2c --i {img_file_equirectangular}  --o {img_file_cubemap} --w {image_clip_size}"
    #     )

    #     # Split Cubemap to simple images
    #     chumk_image_path = f"{image_folder_path}/{image_id}"
    #     if not os.path.exists(chumk_image_path):
    #         os.makedirs(chumk_image_path)
    #     split_cubemap(img_file_cubemap, format_type=1, output_directory=chumk_image_path)
    #     clean_files(image_folder_path, image_id, list_sides)
    return feature


def clean_files(image_folder_path, image_id):
    chumk_image_path = f"{image_folder_path}/{image_id}"

    for file in glob.glob(f"{chumk_image_path}/*.jpg"):
        side = Path(file).stem
        os.rename(
            f"{chumk_image_path}/{side}.jpg",
            f"{image_folder_path}/{image_id}_{side}.jpg",
        )

    # for side in list_sides:
    #     os.rename(
    #         f"{chumk_image_path}/{sides_dict[side]}.jpg",
    #         f"{image_folder_path}/{image_id}_{sides_dict[side]}.jpg",
    #     )
    # # Remove files
    # if os.path.exists(chumk_image_path):
    #     shutil.rmtree(chumk_image_path)


def process_image(input_points, output_images_path, image_clip_size, cube_sides):

    with open(input_points, "r", encoding="utf8") as f:
        features = json.load(f)["features"]

    # Process in parallel
    results = Parallel(n_jobs=-1)(
        delayed(download_process_img)(
            feature, output_images_path, image_clip_size, cube_sides)
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
@click.option("--image_clip_size", help="Image size of the image to clip", default=512)
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
