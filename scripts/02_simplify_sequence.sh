#!/usr/bin/env bash
mapimg="docker run -v $PWD:/mnt/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it devseed/mapimg:v1"

outputDir=data

################ Simplify sequences  ################

priorities="pri_12 pri_13 pri_14"
for priority in $priorities;  do
    echo "======== ${priority} ====="

    # aws s3 cp s3://urban-blight/dallas/mapillary/points_sequences/${priority}_sequences_custom__no__pano_check.geojson  $outputDir/${priority}_sequences_custom__no__pano_check.geojson
    # aws s3 cp s3://urban-blight/dallas/mapillary/points_sequences/${priority}_points__no__pano.geojson  $outputDir/${priority}_points__no__pano.geojson

    $mapimg merge_sequence \
                    --geojson_input=$outputDir/${priority}_sequences_custom__no__pano_check.geojson \
                    --geojson_out=$outputDir/${priority}_sequences__no__pano_merge_check.geojson

    $mapimg simplify_sequence \
                    --geojson_input=$outputDir/${priority}_sequences__no__pano_merge_check.geojson \
                    --buffer=0.000015 \
                    --geojson_out=$outputDir/${priority}_sequences__no__pano_merge_check_filter_buffer.geojson

    $mapimg match_point_sequence \
                    --geojson_polygons=$outputDir/${priority}_sequences__no__pano_merge_check_filter_buffer.geojson \
                    --geojson_points=$outputDir/${priority}_points__no__pano.geojson \
                    --geojson_out=$outputDir/${priority}_points__no__pano_filter_check.geojson



    # aws s3 cp $outputDir/${priority}_points__no__pano_filter_check.geojson s3://urban-blight/dallas/mapillary/points_sequences/${priority}_points__no__pano_filter_check.geojson
done
