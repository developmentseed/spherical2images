import mercantile
import requests
import json
import os
import click
from joblib import Parallel, delayed
from tqdm import tqdm
from vt2geojson.tools import vt_bytes_to_geojson

access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")


def get_points(bbox):
    # define an empty geojson as output
    tile_coverage = "mly1_public"
    tile_layer = "image"
    west, south, east, north = bbox
    tiles = list(mercantile.tiles(west, south, east, north, 14))
    features = []
    for tile in tiles:
        print(tile)
        tile_url = "https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}".format(
            tile_coverage, tile.z, tile.x, tile.y, access_token
        )
        response = requests.get(tile_url)
        data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z, layer=tile_layer)
        # filter pano images in the area
        for feature in data["features"]:
            lng = feature["geometry"]["coordinates"][0]
            lat = feature["geometry"]["coordinates"][1]
            is_pano = feature["properties"]["is_pano"]
            # ensure feature falls inside bounding box since tiles can extend beyond
            if lng > west and lng < east and lat > south and lat < north and is_pano:
                features.append(feature)
    return features


@click.command(short_help="Script to get last updates for adapters")
@click.option(
    "--bbox",
    help="bbox",
    default="-83.2263319287,42.3489816308,-83.2230326577,42.3507715447",
)
@click.option(
    "--output_point",
    help="output point",
    default="data/points.geojson",
)
@click.option(
    "--output_sequences",
    help="output sequences",
    default="data/sequences.geojson",
)
def main(bbox, output_point, output_sequences):
    bbox = [float(item) for item in bbox.split(",")]
    points = get_points(bbox)
    # save points
    with open(output_point, "w") as f:
        json.dump({"type": "FeatureCollection", "features": points}, f)

    # Build sequence linesans and save
    sequences = {}
    points_sorted = sorted(points, key=lambda item: int(item["properties"]["captured_at"]))
    for point in points_sorted:
        sequence_id = str(point["properties"]["sequence_id"])
        if sequence_id not in sequences.keys():
            sequences[sequence_id] = {
                "type": "Feature",
                "properties": {"sequence_id": sequence_id},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [point["geometry"]["coordinates"]],
                },
            }
        else:
            sequences[sequence_id]["geometry"]["coordinates"].append(
                point["geometry"]["coordinates"]
            )

    with open(output_sequences, "w") as f:
        sequences_values = list(sequences.values())
        json.dump({"type": "FeatureCollection", "features": sequences_values}, f)


if __name__ == "__main__":
    main()
