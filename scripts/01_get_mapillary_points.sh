#!/usr/bin/env bash
mkdir -p data

################ Download points and sequences ################
mapimg="docker run -v $PWD:/mnt/ --rm -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed/spherical2images:v1"

#Sunday, May 15, 2022 1:01:01
get_mapillary_points \
    --timestamp_from=1651366800 \
    --output_file_point=data/points.geojson \
    --output_file_sequence=data/sequences.geojson \
    --geojson_boundaries=dallas_boundaries.geojson \
    --field_name=COUNCILPER

# aws s3 sync data/ s3://urban-blight/dallas/mapillary/points_sequences/
