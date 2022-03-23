import click
import json
from tqdm import tqdm
from geojson.feature import FeatureCollection as fc
from joblib import Parallel, delayed
from shapely.geometry import shape, MultiLineString, mapping
from spherical2images.utils import read_geojson, write_geojson, check_geometry


def get_duplicates(l):
    return list(dict.fromkeys(list(set([x for x in l if l.count(x) > 1]))))


def filter_data_dupicate(features_dict):
    def merge_data(same_):
        try:
            same_shp = [shape(i["geometry"]) for i in same_]
            same_shp_line = [i for i in same_shp if i.geom_type == "LineString"]
            same_shp_multi_line = [
                i for i in same_shp if i.geom_type == "MultiLineString"
            ]
            for multi_line in same_shp_multi_line:
                for line in multi_line:
                    same_shp_line.append(line)

            coords = MultiLineString(same_shp_line)
            data_new = same_[0]
            data_new["geometry"] = mapping(coords)
            return data_new
        except Exception as ex:
            return None

    new_features_duplicates = Parallel(n_jobs=-1)(
        delayed(merge_data)(same_)
        for id_, same_ in tqdm(list(features_dict.items()), desc="merge lines")
    )
    return [i for i in new_features_duplicates if i]


def extra_data(features):
    def add_extra_data(feature_):
        geom_shape = shape(feature_["geometry"])
        feature_["properties"]["length"] = geom_shape.length
        feature_["properties"]["points"] = (
            sum([len(i.coords) for i in geom_shape])
            if geom_shape.geom_type == "MultiLineString"
            else len(geom_shape.coords)
        )
        return feature_

    new_features = Parallel(n_jobs=-1)(
        delayed(add_extra_data)(feature)
        for feature in tqdm(features, desc="add extra data")
    )
    return new_features





def process_data(geojson_input, geojson_out):
    """ Start processing sequence geojson files

    Args:
        geojson_input (str): Location for geojson file
        geojson_out (str): Ouput location for geojson file
    """
    features = read_geojson(geojson_input)
    features = [i for i in features if check_geometry(i)]

    initial_objects = len(features)
    id_duplicates = get_duplicates(
        [
            i["properties"].get("sequence_id")
            for i in features
            if i["properties"].get("sequence_id")
        ]
    )

    list_no_duplicates = []
    list_duplicates = {}
    for feature in features:
        fake_id = feature["properties"]["sequence_id"]
        feature["properties"]["id"] = fake_id

        if fake_id in id_duplicates:
            if fake_id in list_duplicates.keys():
                list_duplicates[fake_id].append(feature)
            else:
                list_duplicates[fake_id] = [
                    feature,
                ]
        else:
            list_no_duplicates.append(feature)

    # liberate memory
    del features
    new_features_duplicates = filter_data_dupicate(list_duplicates)
    merge_lines = [*list_no_duplicates, *new_features_duplicates]

    merge_lines_extra = extra_data(merge_lines)

    print("==========")
    print("initial_objects ", initial_objects)
    print("total_objects ", len(merge_lines_extra))
    json.dump(fc(merge_lines_extra), open(geojson_out, "w"))


@click.command(short_help="Script to merge line sequences")
@click.option("--geojson_input", help="Input geojson file", type=str)
@click.option("--geojson_out", help="Output geojson file", type=str)
def run(geojson_input, geojson_out):
    process_data(geojson_input, geojson_out)


if __name__ == "__main__":
    run()
