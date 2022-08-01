#!/usr/bin/env bash
mapimg="docker run -v $PWD:/mnt/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it devseed/mapimg:v1"

outputDir=data
mkdir -p $outputDir

################ Download points from no pano sequences ################

priorities="pri_12 pri_13 pri_14"
for priority in $priorities;  do
    echo "======== ${priority} ====="

    aws s3 cp s3://urban-blight/dallas/mapillary/points_sequences/${priority}_simplify__no__pano_.geojson $outputDir/${priority}_simplify__no__pano_.geojson 

    mkdir -p data/$priority/

    $mapimg lens_correction \
        --input_points=$outputDir/${priority}_simplify__no__pano_.geojson \
        --output_images_path=$outputDir/${priority} \
        --s3_url=https://urban-blight-public-mapillary-images.s3.amazonaws.com/dallas/mapillary/images/${priority} \
        --output_points=$outputDir/${priority}_simplify__no__pano__url__.geojson

    aws s3 sync $outputDir/${priority}  s3://urban-blight-public-mapillary-images/dallas/mapillary/images/${priority}/

done

