#!/usr/bin/env bash
GEO_PY="docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest"

outputDir=data
mkdir -p $outputDir/split_new

################ Download points and sequences ################

priorities=" pri_14"
for priority in $priorities; do
    echo "priority: ${priority}"

    $GEO_PY geo fc_split \
        --geojson_input=$outputDir/${priority}_simplify__no__pano__url__.geojson \
        --size=1000 \
        --geojson_output=$outputDir/split_new/${priority}_no_pano_split_check_url.geojson 

done

aws s3 sync $outputDir/split_new/ s3://ds-data-projects/CPAL/dallas/split_data/           
