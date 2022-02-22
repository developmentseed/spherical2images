#!/usr/bin/env bash
mkdir -p data

################ Download points and sequences ################
./points.sh

################ Simplify sequence ################
# TODO

################ Simplify points ################
./simplify_points.sh

################ Download and clip images ################

./clip_pano.sh