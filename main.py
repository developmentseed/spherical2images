import mercantile
import requests
import json
import os
import click
from vt2geojson.tools import vt_bytes_to_geojson


def process_image(bbox, cube):
    # define an empty geojson as output
    output = {"type": "FeatureCollection", "features": []}
    tile_coverage = "mly1_public"
    tile_layer = "image"
    access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")
    west, south, east, north = bbox
    tiles = list(mercantile.tiles(west, south, east, north, 14))

    for tile in tiles:
        tile_url = (
            "https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}".format(
                tile_coverage, tile.z, tile.x, tile.y, access_token
            )
        )
        response = requests.get(tile_url)
        data = vt_bytes_to_geojson(
            response.content, tile.x, tile.y, tile.z, layer=tile_layer
        )

        # filter pano images in the area
        features = []
        for feature in data["features"]:
            lng = feature["geometry"]["coordinates"][0]
            lat = feature["geometry"]["coordinates"][1]
            is_pano = feature["properties"]["is_pano"]
            # ensure feature falls inside bounding box since tiles can extend beyond
            if lng > west and lng < east and lat > south and lat < north and is_pano:
                features.append(feature)
                output["features"].append(feature)


        for feature in features:
            sequence_id = feature["properties"]["sequence_id"]

            if not os.path.exists(f"data/{sequence_id}"):
                os.makedirs(f"data/{sequence_id}")

            # request the URL of each image
            image_id = feature["properties"]["id"]
            header = {"Authorization": "OAuth {}".format(access_token)}
            url = "https://graph.mapillary.com/{}?fields=thumb_2048_url".format(
                image_id
            )

            r = requests.get(url, headers=header)
            data = r.json()
            image_url = data["thumb_2048_url"]

            img_file = "data/{}/{}.jpg".format(sequence_id, image_id)
            with open(img_file, "wb") as handler:
                image_data = requests.get(image_url, stream=True).content
                handler.write(image_data)
                
            os.system(f'sphericalpano2cube -d 512 {img_file} {img_file}')
            

    return output


@click.command(short_help="Script to get last updates for adapters")
@click.option(
    "--bbox",
    help="bbox",
    default="-83.2263319287,42.3489816308,-83.2230326577,42.3507715447",
)
@click.option(
    "--cube",
    help="Argumeent to split the pano image into chunk of images",
    default=True,
    type=bool,
)
def main(bbox, cube):
    bbox = [float(item) for item in bbox.split(",")]
    output = process_image(bbox, cube)

    # with open("list.json", "w") as f:
    #     json.dump(output, f)


if __name__ == "__main__":
    main()
