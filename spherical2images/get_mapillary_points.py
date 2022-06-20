import json

import click
from spherical2images.utils import get_mapillary_points_bbox, build_mapillary_sequence
from spherical2images.utils import write_geojson
from shapely.geometry import shape


def add_name_path(path_, name_):
    """Script add a name in a path file

    Args:
        path_ (str): a path
        name_ (str): geojson_boundaries for multiple bounds
    Returns:
        str : a path with name
    """
    name_extension = path_.strip().split("/")[-1]
    return path_.replace(name_extension, f"{name_}_{name_extension}")


@click.command(short_help="Script to get points and sequence for a bbox from mapillary")
@click.option(
    "--bbox",
    help="bbox",
    default="-83.2263319287,42.3489816308,-83.2230326577,42.3507715447",
    required=False,
)
@click.option(
    "--geojson_boundaries", help="geojson_boundaries", default="", required=False
)
@click.option("--field_name", help="field_name", default="", required=False)
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
def main(
        bbox,
        geojson_boundaries,
        field_name,
        timestamp_from,
        only_pano,
        output_file_point,
        output_file_sequence,
):
    """Script to get points and sequence for a bbox from mapillary

    Args:
        bbox (str): bbox
        geojson_boundaries (str): geojson_boundaries for multiple bounds
        field_name (str): field_name
        timestamp_from (int): Timestamp to filter
        only_pano (bool): flag to filter pano points
        output_file_point (str): Pathfile for geojson point file
        output_file_sequence (str): Pathfile for geojson sequence file
    """
    boundaries = []

    if geojson_boundaries:
        features = json.load(open(geojson_boundaries)).get("features")
        for feature in features:
            props = feature.get("properties")
            name = props.get(field_name, "").strip().replace(" ", "_")
            geom = shape(feature.get("geometry"))
            boundaries.append(
                {
                    "bbox": geom.bounds,
                    "output_file_point": add_name_path(output_file_point, name),
                    "output_file_sequence": add_name_path(output_file_sequence, name),
                    "geom": geom,
                    "name_file": name,
                }
            )
    else:
        boundaries.append(
            {
                "bbox": tuple([float(item.strip()) for item in bbox.split(",")]),
                "output_file_point": output_file_point,
                "output_file_sequence": output_file_sequence,
                "geom": None,
                "name_file": output_file_point.split("/")[-1],
            }
        )
    total_no_pano = 0
    total_pano = 0
    for boundarie in boundaries:
        points = get_mapillary_points_bbox(
            boundarie.get("bbox"),
            only_pano,
            timestamp_from,
            boundarie.get("geom"),
            boundarie.get("name_file"),
        )
        total = len(points)
        pano = [i for i in points if i.get("properties").get("is_pano")]
        no_pano = [i for i in points if not i.get("properties").get("is_pano")]
        total_no_pano += len(no_pano)
        total_pano += len(pano)

        print("=" * 10)
        print("city", boundarie.get("name_file"))
        print("total points", total)
        print("pano", len(pano))
        print("no pano", len(no_pano))
        # separate points
        write_geojson(boundarie.get("output_file_point").replace(".geojson", "__pano.geojson"), pano)
        write_geojson(boundarie.get("output_file_point").replace(".geojson", "__no__pano.geojson"), no_pano)

        sequences_pano = build_mapillary_sequence(pano)
        sequences_no_pano = build_mapillary_sequence(no_pano)

        print("total sequences pano", len(sequences_pano))
        print("total sequences no pano", len(sequences_no_pano))

        write_geojson(boundarie.get("output_file_sequence").replace(".geojson", "__pano.geojson"), sequences_pano)
        write_geojson(boundarie.get("output_file_sequence").replace(".geojson", "__no__pano.geojson"), sequences_no_pano)

    print("="*10)
    print("="*10)
    print("pano", total_pano)
    print("no pano", total_no_pano)


if __name__ == "__main__":
    main()
