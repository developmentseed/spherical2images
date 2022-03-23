import cv2
from PIL import Image
from smart_open import open
import pathlib
import mercantile
import requests
import os
import json
from vt2geojson.tools import vt_bytes_to_geojson
from geojson import FeatureCollection
from shapely.geometry import shape

access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")


def get_mapillary_points_bbox(bbox):
    """Get a bbox and returns a feature list of mapillary points that are pano images

    Args:
        bbox (tuple): bounds area to get the points

    Returns:
        list: list of features
    """
    mapillary_URL = "https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}"
    tile_coverage = "mly1_public"
    tile_layer = "image"
    west, south, east, north = bbox
    tiles = list(mercantile.tiles(west, south, east, north, 14))
    features = []
    for tile in tiles:
        tile_url = mapillary_URL.format(
            tile_coverage, tile.z, tile.x, tile.y, access_token
        )
        response = requests.get(tile_url)
        data = vt_bytes_to_geojson(
            response.content, tile.x, tile.y, tile.z, layer=tile_layer
        )
        # Filter pano images in the area
        for feature in data["features"]:
            lng = feature["geometry"]["coordinates"][0]
            lat = feature["geometry"]["coordinates"][1]
            is_pano = feature["properties"]["is_pano"]
            if lng > west and lng < east and lat > south and lat < north and is_pano:
                features.append(feature)
    return features


def build_mapillary_sequence(points):
    """Build sequence  using points, return linestring

    Args:
        points (fc): Feature collection of points

    Returns:
        list[fc]: Feature collection of linestring
    """
    sequences = {}
    points_sorted = sorted(
        points, key=lambda item: int(item["properties"]["captured_at"])
    )
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

    return list(sequences.values())


def read_geojson(input_file):
    """Read a geojson file and return a list of features

    Args:
        input_file (str): Location on geojson file

    Returns:
        list: list fo features
    """
    fc = []
    with open(input_file, "r", encoding="utf8") as f:
        cf = json.load(f)["features"]
    return cf


def write_geojson(output_file, list_features):
    """Write geojson files

    Args:
        output_file (str): Location of ouput file
        list_features (list): List of features
    """
    with open(output_file, "w") as f:
        json.dump(FeatureCollection(list_features), f)


def check_geometry(feature):
    """Verify if geometry is valid

    Args:
        feat (obj): Feature

    Returns:
        Bool: Return false or true acoording to the geometry
    """
    try:
        geom_shape = shape(feature["geometry"])
        return geom_shape.is_valid
    except Exception:
        return False