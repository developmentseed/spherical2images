#!/usr/bin/env bash
mkdir -p data

################ Download points and sequences ################
./01_get_mapillary_points.sh

################ Simplify sequence ################
./02_simplify_sequence.sh

################ Simplify points ################
./03_simplify_points.sh

################ Download and clip images ################

./04_clip_mapillary_pano.sh
