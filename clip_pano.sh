#!/usr/bin/env bash
mkdir -p data

################ Download points and sequences ################

python clip_pano.py \
    --input_points=data/Weatherby_simplify.geojson \
    --output_images_path=data/Weatherby \
    --image_clip_size=1024 \
    --output_points=data/Weatherby_images.geojson

aws s3 sync data/Weatherby/ s3://ds-data-projects/CPAL/mapillary/images/Weatherby/image/ --exclude="*" --include="*_left.jpg" --include="*_right.jpg"
