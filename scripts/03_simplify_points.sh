#!/usr/bin/env bash
outputDir=data
mkdir -p $outputDir

mapimg="docker run -v $PWD:/mnt/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed/spherical2images:v1"

aws s3 sync s3://urban-blight/detroit/mapillary/points_sequences/ $outputDir/

$mapimg simplify_points \
    --input_points=$outputDir/Warrendale_points_filter.geojson \
    --output_points=$outputDir/Warrendale_simplify.geojson

$mapimg simplify_points \
    --input_points=$outputDir/Belmont_points_filter.geojson \
    --output_points=$outputDir/Belmont_simplify.geojson

$mapimg simplify_points \
    --input_points=$outputDir/Franklin_Park_points_filter.geojson \
    --output_points=$outputDir/Franklin_Park_simplify.geojson

$mapimg simplify_points \
    --input_points=$outputDir/Weatherby_points_filter.geojson \
    --output_points=$outputDir/Weatherby_simplify.geojson

$mapimg simplify_points \
    --input_points=$outputDir/Petoskey_sego_points_filter.geojson \
    --output_points=$outputDir/Petoskey_sego_simplify.geojson

$mapimg simplify_points \
    --input_points=$outputDir/Carbon_Works_points_filter.geojson \
    --output_points=$outputDir/Carbon_Works_simplify.geojson

$mapimg simplify_points \
    --input_points=$outputDir/Brush_Park_points_filter.geojson \
    --output_points=$outputDir/Brush_Park_simplify.geojson

$mapimg simplify_points \
    --input_points=$outputDir/Fiskhorn_points_filter.geojson \
    --output_points=$outputDir/Fiskhorn_simplify.geojson

aws s3 sync $outputDir/ s3://urban-blight/detroit/mapillary/points_sequences/
