#!/usr/bin/env bash
mapimg="docker run -v $PWD:/mnt/ --rm -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed/spherical2images:v1"

outputDir=data
mkdir -p $outputDir

################ Download points and sequences ################

#Sunday, May 15, 2022 1:01:01
$mapimg get_mapillary_points \
    --timestamp_from=1651366800000 \
    --organization_ids=1805883732926354 \
    --output_file_point=$outputDir/points.geojson \
    --output_file_sequence=$outputDir/sequences.geojson \
    --geojson_boundaries=priority_area.geojson \
    --field_name=area
