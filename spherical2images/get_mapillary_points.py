import click
from spherical2images.utils import get_mapillary_points_bbox, build_mapillary_sequence
from spherical2images.utils import write_geojson


@click.command(short_help="Script to get points and sequence for a bbox from mapillary")
@click.option(
    "--bbox",
    help="bbox",
    default="-83.2263319287,42.3489816308,-83.2230326577,42.3507715447",
)
@click.option(
    "--timestamp_from", help="timestamp_from", default=0, type=int, required=False
)
@click.option(
    "--only_pano",
    help="timestamp_from",
    default=False,
    type=bool,
    required=False,
    is_flag=True,
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
def main(bbox, timestamp_from, only_pano, output_file_point, output_file_sequence):
    """Script to get points and sequence for a bbox from mapillary

    Args:
        bbox (str): bbox
        timestamp_from (int): Timestamp to filter
        only_pano (bool): flag to filter pano points
        output_file_point (str): Pathfile for geojson point file
        output_file_sequence (str): Pathfile for geojson sequence file
    """
    bbox = tuple([float(item) for item in bbox.split(",")])
    points = get_mapillary_points_bbox(bbox, only_pano, timestamp_from)
    write_geojson(output_file_point, points)
    sequences = build_mapillary_sequence(points)
    write_geojson(output_file_sequence, sequences)


if __name__ == "__main__":
    main()
