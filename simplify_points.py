import json
import click
import shapely.geometry


def distance(current_point, next_point):
    current_geo = shapely.geometry.shape(current_point["geometry"])
    next_geo = shapely.geometry.shape(next_point["geometry"])
    dist = current_geo.distance(next_geo)
    return dist


@click.command(short_help="Script to get last updates for adapters")
@click.option(
    "--input_points",
    help="input points",
    default="data/points.geojson",
)
@click.option(
    "--output_points",
    help="output points",
    default="data/output_points.geojson",
)
def main(input_points, output_points):
    with open(input_points, "r", encoding="utf8") as f:
        features = json.load(f)["features"]
    sequences = {}
    # Sort by sequence id
    for feature in features:
        sequence_id = str(feature["properties"]["sequence_id"])
        if sequence_id not in sequences.keys():
            sequences[sequence_id] = [feature]
        else:
            sequences[sequence_id].append(feature)

    new_points = []
    for sequence in sequences.values():
        points_sorted = sorted(sequence, key=lambda item: int(item["properties"]["captured_at"]))
        for index, point in enumerate(points_sorted):
            if index == 0:
                current_point = point
            if len(points_sorted) == index + 1:
                next_point = point
            else:
                next_point = points_sorted[index + 1]
            d = distance(current_point, next_point)
            if d > 0.0001:
                current_point = next_point
            new_points.append(current_point)

    with open(output_points, "w") as f:
        json.dump({"type": "FeatureCollection", "features": new_points}, f)


if __name__ == "__main__":
    main()
