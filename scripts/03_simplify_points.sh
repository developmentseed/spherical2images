#!/usr/bin/env bash
mapimg="docker run -v $PWD:/mnt/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed/spherical2images:v1"

outputDir=data

################ Simplify points ################

priorities="pri_3"
for priority in $priorities;  do
  echo "======== ${priority} ====="
  # aws s3 cp s3://urban-blight/dallas/mapillary/points_sequences/${priority}_points__no__pano_filter_check.geojson  $outputDir/${priority}_points__no__pano_filter_check.geojson

  $mapimg simplify_points \
      --input_points=$outputDir/${priority}_points__no__pano_filter_check.geojson \
      --output_points=$outputDir/${priority}_simplify__no__pano_.geojson

      # aws s3 cp $outputDir/${priority}_simplify__no__pano_.geojson s3://urban-blight/dallas/mapillary/points_sequences/${priority}_simplify__no__pano_.geojson

done

