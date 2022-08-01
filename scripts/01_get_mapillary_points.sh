#!/usr/bin/env bash
mapimg="docker run -v $PWD:/mnt/ --rm -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed/spherical2images:v1"

mkdir -p data

################ Download points and sequences ################

#Sunday, May 15, 2022 1:01:01
$mapimg get_mapillary_points \
    --timestamp_from=1651366800 \
    --organization_ids=1805883732926354 \
    --output_file_point=data/points.geojson \
    --output_file_sequence=data/sequences.geojson \
    --geojson_boundaries=areas_prioritarias_7_plus.geojson \
    --field_name=area
