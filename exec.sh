#!/usr/bin/env bash
mkdir -p data

################ Download points and sequences ################
./points.sh

################ Simplify sequence ################
./simplify_sequence.sh

################ Simplify points ################
./simplify_points.sh

################ Download and clip images ################

./clip_pano.sh
