#!/usr/bin/env bash
mapimg="docker run -v $PWD:/mnt/ --rm -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed/spherical2images:v1"

outputDir=data
mkdir -p $outputDir

$mapimg clip_mapillary_pano \
    --input_images_folder=$outputDir/Road_S1_SPL \
    --image_clip_size=1024 \
    --output_file_points=$outputDir/points__pano_output_folder.geojson \
    --output_images_path=$outputDir/clip_raw_images_spl_1024 \
    --cube_sides=right,left
