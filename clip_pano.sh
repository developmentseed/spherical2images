#!/usr/bin/env bash
mkdir -p data

################ Download points and sequences ################

python clip_pano.py \
    --input_points=s3://urban-blight/detroit/mapillary/points_sequences/Belmont_simplify_validated.geojson \
    --output_images_path=data/Belmont \
    --image_clip_size=1024 \
    --output_points=s3://urban-blight/detroit/mapillary/points_sequences/Belmont_point_images.geojsonn

aws s3 sync data/Belmont/ s3://urban-blight/detroit/mapillary/images/Belmont/ --exclude="*" --include="*_left.jpg" --include="*_right.jpg"
