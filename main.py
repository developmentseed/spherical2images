import mercantile
import requests
import json
import os
import click
from joblib import Parallel, delayed
from tqdm import tqdm
from vt2geojson.tools import vt_bytes_to_geojson

access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")
storage_path = "/mnt/data"
sides_dict = {
    "0": "front",
    "1": "left",
    "2": "right",
    "3": "back",
    "4": "over",
    "5": "under",
}


def download_process_img(feature, cube_sides):
    """Download and clip the spherical image

    Args:
        feature (dict): feture
        cube_sides (str): list of sited to clip

    Returns:
        [dict]: feature
    """
    sequence_id = feature["properties"]["sequence_id"]

    if not os.path.exists(f"{storage_path}/{sequence_id}"):
        os.makedirs(f"{storage_path}/{sequence_id}")

    # request the URL of each image
    image_id = feature["properties"]["id"]

    # Check if mapillary image exist and download
    img_file = f"{storage_path}/{sequence_id}/{image_id}.jpg"
    if not os.path.isfile(img_file):
        header = {"Authorization": "OAuth {}".format(access_token)}
        url = "https://graph.mapillary.com/{}?fields=thumb_2048_url".format(image_id)
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
            img_cube_chunk = f"{storage_path}/{sequence_id}/{image_id}_{sides_dict[i]}.jpg"
            if not os.path.isfile(img_cube_chunk):
                list_sides.append(i)
            else:
                print(f"File exist..{img_cube_chunk}")

    # Split spherical image into chunks
    if len(list_sides) > 0:
        str_sides = ",".join(list_sides)
        os.system(f"sphericalpano2cube -d 512 -s {cube_sides} {img_file} {img_file}")
    return feature


def process_image(bbox, cube_sides):
    # define an empty geojson as output
    tile_coverage = "mly1_public"
    tile_layer = "image"
    west, south, east, north = bbox
    tiles = list(mercantile.tiles(west, south, east, north, 14))

    for tile in tiles:
        tile_url = "https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}".format(
            tile_coverage, tile.z, tile.x, tile.y, access_token
        )
        response = requests.get(tile_url)
        data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z, layer=tile_layer)

        # filter pano images in the area
        features = []
        for feature in data["features"]:
            lng = feature["geometry"]["coordinates"][0]
            lat = feature["geometry"]["coordinates"][1]
            is_pano = feature["properties"]["is_pano"]
            # ensure feature falls inside bounding box since tiles can extend beyond
            if lng > west and lng < east and lat > south and lat < north and is_pano:
                features.append(feature)
        # Process in parallel
        # results = Parallel(n_jobs=-1)(
        #     delayed(download_process_img)(feature, cube_sides)
        #     for feature in tqdm(features[:100], desc=f"Processing images for...", total=len(features[:100]))
        # )
    return features


@click.command(short_help="Script to get last updates for adapters")
@click.option(
    "--bbox",
    help="bbox",
    default="-83.2263319287,42.3489816308,-83.2230326577,42.3507715447",
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
def main(bbox, cube_sides):
    bbox = [float(item) for item in bbox.split(",")]
    output = process_image(bbox, cube_sides)

    with open(f"{storage_path}/list.geojson", "w") as f:
        json.dump({"type": "FeatureCollection", "features": output}, f)


if __name__ == "__main__":
    main()
