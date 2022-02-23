#!/usr/bin/env bash
mkdir -p data

################ Download points and sequences ################
#Belmont
neighborhoods="Brush_Park Fiskhorn Carbon_Works Franklin_Park Petoskey_sego Warrendale Weatherby"
for neighborhood in $neighborhoods; do
    echo "NEIGHBORHOOD: $neighborhood"
    python clip_pano.py \
        --input_points=s3://urban-blight/detroit/mapillary/points_sequences/${neighborhood}_simplify_validated.geojson \
        --image_clip_size=1024 \
        --output_points=s3://urban-blight/detroit/mapillary/points_sequences/${neighborhood}_point_images.geojson \
        --output_images_path=data/$neighborhood

    aws s3 sync data/$neighborhood/ s3://urban-blight-public-mapillary-images/detroit/mapillary/images/$neighborhood/ --exclude="*" --include="*_left.jpg" --include="*_right.jpg"

done
