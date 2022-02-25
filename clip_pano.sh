#!/usr/bin/env bash
mkdir -p data

################ Download points and sequences ################
#Belmont Brush_Park Fiskhorn Carbon_Works Franklin_Park Petoskey_sego Warrendale
neighborhoods="Weatherby"
for neighborhood in $neighborhoods; do
    echo "NEIGHBORHOOD: $neighborhood"
    mkdir -p data/$neighborhood
    python clip_pano.py \
        --input_points=s3://urban-blight/detroit/mapillary/points_sequences/${neighborhood}_simplify_validated.geojson \
        --image_clip_size=1024 \
        --output_points=s3://urban-blight/detroit/mapillary/points_sequences/${neighborhood}_point_images.geojson \
        --output_images_path=s3://urban-blight-public-mapillary-images/detroit/mapillary/images/$neighborhood \
        --cube_sides=right,left
done
