import json

import click
from spherical2images.utils import build_mapillary_sequence
from spherical2images.utils import write_geojson


@click.command(short_help="create custom sequences")
@click.option("--geojson_points", help="geojson_points", default="", required=False)
@click.option(
    "--output_file_sequence",
    help="Path for custom sequence file",
    default="data/sequences.geojson",
    type=click.Path(),
)
def run(geojson_points, output_file_sequence):
    features = json.load(open(geojson_points)).get("features")
    sequences = build_mapillary_sequence(features, True)
    write_geojson(output_file_sequence, sequences)


if __name__ == "__main__":
    run()
