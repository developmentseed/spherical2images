#!/usr/bin/env bash
mkdir -p data

################ Download points and sequences ################
mapimg="docker run -v $PWD:/mnt/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it devseed/mapimg:v1"

$mapimg python clip_pano.py \
    --input_points=data/Weatherby_simplify.geojson \
    --output_images_path=data/Weatherby \
    --image_clip_size=512 \
    --output_points=data/Weatherby_images.geojson

# aws s3 sync data/Weatherby s3://ds-data-projects/CPAL/mapillary/images/Weatherby/
 