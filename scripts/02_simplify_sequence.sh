#!/usr/bin/env bash
mapimg="docker run -v $PWD:/mnt/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed/spherical2images:v1"

outputDir=data

neighborhoods=(Belmont Brush_Park Carbon_Works Franklin_Park Petoskey_sego Warrendale Weatherby Fiskhorn)
for neighborhood in "${neighborhoods[@]}"; do
        echo "======== ${neighborhood} ====="

        $mapimg merge_sequence \
                --geojson_input=$outputDir/${neighborhood}_sequences.geojson \
                --geojson_out=$outputDir/${neighborhood}_sequences_merge.geojson

        $mapimg simplify_sequence \
                --geojson_input=$outputDir/${neighborhood}_sequences_merge.geojson \
                --geojson_out=$outputDir/${neighborhood}_sequences_filter_buffer.geojson

        $mapimg match_point_sequence \
                --geojson_polygons=$outputDir/${neighborhood}_sequences_filter_buffer.geojson \
                --geojson_points=$outputDir/${neighborhood}_points.geojson \
                --geojson_out=$outputDir/${neighborhood}_points_filter.geojson

done
