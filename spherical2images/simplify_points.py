import click
import random
from spherical2images.utils import read_geojson, write_geojson, geom_data
from copy import deepcopy


def distance(current_point, next_point):
    """calculate the distance between two points

    Args:
        current_point (geom): feature object (point)
        next_point (geom): feature object (point)
    """
    dist = current_point.distance(next_point)
    return dist


@click.command(short_help="Script to get last updates for adapters")
@click.option(
    "--input_points",
    help="Pathfile for geojson input (points)",
    default="data/points.geojson",
)
@click.option(
    "--output_points",
    help="Pathfile for geojson output (points)",
    default="data/output_points.geojson",
)
def main(input_points, output_points):
    features = read_geojson(input_points)
    features = geom_data(features)
    sequences = {}
    # Sort by sequence id
    for feature in features:
        sequence_id = str(feature["properties"]["sequence_id"])
        if sequence_id not in sequences.keys():
            sequences[sequence_id] = []
        sequences[sequence_id].append(feature)

    new_points = []
    for sequence in sequences.values():
        points_sorted = sorted(
            sequence, key=lambda item: int(item["properties"]["captured_at"])
        )
        for index, point in enumerate(points_sorted):
            if index == 0:
                current_point = point
            if len(points_sorted) == index + 1:
                next_point = point
            else:
                next_point = points_sorted[index + 1]
            d = distance(current_point.get("geom"), next_point.get("geom"))
            if d > 0.0001:
                current_point = next_point
            new_points.append(deepcopy(current_point))

    # remove points duplicates
    points_dict = {str(i["geom"].wkb_hex): i for i in new_points}
    filter_data = list(points_dict.values())
    # random.shuffle(filter_data)

    for i in filter_data:
        if "geom" in i.keys():
            del i["geom"]
    print("===================")
    print("Simplify points")
    print("initial data", len(features))
    print("result data", len(filter_data))

    write_geojson(output_points, filter_data)


if __name__ == "__main__":
    main()
