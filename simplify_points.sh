#!/usr/bin/env bash

mkdir -p data

python simplify_points.py \
--input_points=data/Brush_Park_points_filter.geojson \
--output_points=data/Brush_Park_points-simplify.geojson