#!/usr/bin/env bash
mapimg="docker run -v $PWD:/mnt/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it devseed/mapimg:v1"

aws s3 sync s3://urban-blight/detroit/mapillary/points_sequences/ data/

$mapimg simplify_points \
    --input_points=data/Warrendale_points_filter.geojson \
    --output_points=data/Warrendale_simplify.geojson

$mapimg simplify_points \
    --input_points=data/Belmont_points_filter.geojson \
    --output_points=data/Belmont_simplify.geojson

$mapimg simplify_points \
    --input_points=data/Franklin_Park_points_filter.geojson \
    --output_points=data/Franklin_Park_simplify.geojson

$mapimg simplify_points \
    --input_points=data/Weatherby_points_filter.geojson \
    --output_points=data/Weatherby_simplify.geojson

$mapimg simplify_points \
    --input_points=data/Petoskey_sego_points_filter.geojson \
    --output_points=data/Petoskey_sego_simplify.geojson

$mapimg simplify_points \
    --input_points=data/Carbon_Works_points_filter.geojson \
    --output_points=data/Carbon_Works_simplify.geojson

$mapimg simplify_points \
    --input_points=data/Brush_Park_points_filter.geojson \
    --output_points=data/Brush_Park_simplify.geojson

$mapimg simplify_points \
    --input_points=data/Fiskhorn_points_filter.geojson \
    --output_points=data/Fiskhorn_simplify.geojson

aws s3 sync data/ s3://urban-blight/detroit/mapillary/points_sequences/
