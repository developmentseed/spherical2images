import click
import json
from tqdm import tqdm
from geojson.feature import FeatureCollection as fc
from joblib import Parallel, delayed
from shapely.geometry import shape

import logging

logger = logging.getLogger("__name__")


def shp_data(features):
    def shp_data_feat(feature_):
        geom_shape = shape(feature_["geometry"])
        feature_["geom"] = geom_shape
        return feature_

    new_features = Parallel(n_jobs=-1)(
        delayed(shp_data_feat)(feature) for feature in tqdm(features, desc="shp data")
    )
    return new_features


def poly_in_point(features, features_poly):
    def feature_in_seq(feature_, features_poly_):
        feature_shape = feature_["geom"]
        feature_seq = feature_["properties"]["sequence_id"]
        for feature_poly in features_poly_:
            feature_poly_shape = feature_poly["geom"]
            feature_poly_seq = feature_poly["properties"]["sequence_id"]
            is_intersects = feature_poly_shape.intersects(feature_shape)
            if feature_seq == feature_poly_seq and is_intersects:
                return feature_
        return None

    new_features = Parallel(n_jobs=-1, prefer="threads")(
        delayed(feature_in_seq)(feature, features_poly)
        for feature in tqdm(features, desc="points in polygons")
    )
    return [i for i in new_features if i]


def process_data(geojson_polygons, geojson_points, geojson_out):
    features_poly = shp_data(json.load(open(geojson_polygons)).get("features"))
    features_points = shp_data(json.load(open(geojson_points)).get("features"))
    filter_data = poly_in_point(features_points, features_poly)
    for i in filter_data:
        if "geom" in i.keys():
            del i["geom"]
    print("==========")
    print("original_data ", len(features_points))
    print("total_filter ", len(filter_data))
    json.dump(fc(filter_data), open(geojson_out, "w"))


@click.command(short_help="Script to filter point in polygons and secuence_id")
@click.option("--geojson_polygons", help="Input geojson file", type=str)
@click.option("--geojson_points", help="Input geojson points", type=str)
@click.option("--geojson_out", help="Output geojson file", type=str)
def run(geojson_polygons, geojson_points, geojson_out):
    process_data(geojson_polygons, geojson_points, geojson_out)


if __name__ == "__main__":
    run()
