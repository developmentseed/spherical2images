import click
import json
from spherical2images.utils import get_mapillary_points_bbox, build_mapillary_sequence
from spherical2images.utils import write_geojson


@click.command(short_help="Script to get points and sequence for a bbox from mapillary")
@click.option(
    "--bbox",
    help="bbox",
    default="-83.2263319287,42.3489816308,-83.2230326577,42.3507715447",
)
@click.option(
    "--output_file_point",
    help="Pathfile for geojson point file",
    default="data/points.geojson",
    type=click.Path(),
)
@click.option(
    "--output_file_sequence",
    help="Pathfile for geojson sequence file",
    default="data/sequences.geojson",
    type=click.Path(),
)
def main(bbox, output_file_point, output_file_sequence):
    bbox = [float(item) for item in bbox.split(",")]
    points = get_mapillary_points_bbox(bbox)
    write_geojson(output_file_point, points)
    sequences = build_mapillary_sequence(points)
    write_geojson(output_file_sequence, sequences)


if __name__ == "__main__":
    main()
