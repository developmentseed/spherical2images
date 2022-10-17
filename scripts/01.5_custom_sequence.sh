#!/usr/bin/env bash
mapimg="docker run -v $PWD:/mnt/ --rm -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed/spherical2images:v1"

outputDir=data
mkdir -p $outputDir

################ Create custom sequences to check and remove ################

priorities="pri_12  pri_13 pri_14"
for priority in $priorities; do
    echo "======== ${priority} ====="

    $mapimg create_custom_sequences \
        --geojson_points=$outputDir/${priority}_points__no__pano.geojson \
        --output_file_sequence=$outputDir/${priority}_sequences_custom__no__pano.geojson
    
    # aws s3 cp $outputDir/${priority}_points__no__pano.geojson s3://urban-blight/dallas/mapillary/points_sequences/${priority}_points__no__pano.geojson  

done

# upload check files, review is a manual process
# aws s3 cp $outputDir/${priority}_sequences_custom__no__pano_check.geojson s3://urban-blight/dallas/mapillary/points_sequences/${priority}_sequences_custom__no__pano_check.geojson 
