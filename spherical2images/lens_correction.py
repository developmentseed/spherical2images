import click
import lensfunpy
import cv2
from spherical2images.utils_images import correct_image
from spherical2images.utils import read_geojson, write_geojson
import os
import requests
from joblib import Parallel, delayed
from tqdm import tqdm
from uuid import uuid4

CAM_MAKER = "FUJIFILM"
CAM_MODEL = "X-T1"
LENS_MAKER = "Samyang"
LENS_MODEL = "8mm f_2.8 UMC Fish-eye"
db = lensfunpy.Database()
camera = db.find_cameras(CAM_MAKER, CAM_MODEL)[0]
lens = db.find_lenses(camera, LENS_MAKER, LENS_MODEL)[0]

FOCAL_LENGTH = 28.0
APERTURE = 1.4
DISTANCE = 10
access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")


def feature_image_correction(feature, output_images_path, header, s3_url):
    """Function to run in parallel mode to download flat image and correct lents

    Args:
        feature (dict): features dict
        output_images_path (str): Path to save images
        header (dict): header with auth
        s3_url (str): url (http) for public bucket
    Returns:
        dict: feature dict with url field
    """
    sequence_id = feature["properties"]["sequence_id"]
    image_id = feature["properties"]["id"]
    uuid_id_ = str(uuid4())
    feature["uuid_id_"] = uuid_id_
    feature["properties"]["uuid_id_"] = uuid_id_

    image_folder_path = f"{output_images_path}/{sequence_id}"
    if image_folder_path[:5] not in ["s3://", "gs://"]:
        os.makedirs(image_folder_path, exist_ok=True)

    file_name = f"{image_folder_path}/{image_id}_original.jpg"
    file_name_fixed = f"{image_folder_path}/{image_id}_fixed.jpg"
    url = "https://graph.mapillary.com/{}?fields=thumb_1024_url".format(image_id)

    feature["properties"]["url"] = file_name_fixed.replace(output_images_path, s3_url)

    if os.path.exists(file_name) and os.path.exists(file_name_fixed):
        return feature

    try:
        r = requests.get(url, headers=header, timeout=30)
        data = r.json()
        image_url = data["thumb_1024_url"]
        # file original
        with open(file_name, "wb") as handler:
            image_data = requests.get(image_url, stream=True).content
            handler.write(image_data)
        # correct_image
        fixed_im = correct_image(
            file_name, camera, lens, FOCAL_LENGTH, APERTURE, DISTANCE
        )
        cv2.imwrite(file_name_fixed, fixed_im)

    except Exception as err:
        print(err, image_id, url)
    return feature


@click.command(short_help="Script to correction lens")
@click.option(
    "--input_points",
    help="Pathfile for geojson input (points)",
    default="data/points.geojson",
)
@click.option(
    "--s3_url", help="http url  to s3 public bucket",
)
@click.option(
    "--output_images_path", help="Path to save images", default="data/images",
)
@click.option(
    "--output_points",
    help="Pathfile for geojson output (points)",
    default="data/output_points.geojson",
)
def main(input_points, output_images_path, s3_url, output_points):
    features = read_geojson(input_points)
    header = {"Authorization": "OAuth {}".format(access_token)}
    if s3_url.endswith("/"):
        s3_url = s3_url[:-1]
    new_features = Parallel(n_jobs=-1, prefer="threads")(
        delayed(feature_image_correction)(feature, output_images_path, header, s3_url)
        for feature in tqdm(features, desc="process image")
    )
    write_geojson(output_points, new_features)


if __name__ == "__main__":
    main()
