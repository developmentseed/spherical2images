#!/usr/bin/env bash

mkdir -p data

python points.py \
--output_point=data/Warrendale_points.geojson \
--output_sequences=data/Warrendale_sequences.geojson \
--bbox=-83.2469680005052,42.3289420003625,-83.2157740004676,42.3578449996934

python points.py \
--output_point=data/Belmont_points.geojson \
--output_sequences=data/Belmont_sequences.geojson \
--bbox=-83.1990169996341,42.4015130001324,-83.1889085119652,42.4090552735721

python points.py \
--output_point=data/Franklin_Park_points.geojson \
--output_sequences=data/Franklin_Park_sequences.geojson \
--bbox=-83.247259999685,42.3573640002526,-83.2165219997569,42.3722550003566

python points.py \
--output_point=data/Weatherby_points.geojson \
--output_sequences=data/Weatherby_sequences.geojson \
--bbox=-83.2464110001133,42.3718289995413,-83.2259659991186,42.3804620001946

python points.py \
--output_point=data/Petoskey_sego_points.geojson \
--output_sequences=data/Petoskey_sego_sequences.geojson \
--bbox=-83.1312979996075,42.3559539994756,-83.1088430001982,42.3701500001189

python points.py \
--output_point=data/Carbon_Works_points.geojson \
--output_sequences=data/Carbon_Works_sequences.geojson \
--bbox=-83.1444729996865,42.2791339994442,-83.1177030003022,42.2983520001828

python points.py \
--output_point=data/Brush_Park_points.geojson \
--output_sequences=data/Brush_Park_sequences.geojson \
--bbox=-83.0578769999087,42.3398419998626,-83.0478359999721,42.3496030001848

python points.py \
--output_point=data/Fiskhorn_points.geojson \
--output_sequences=data/Fiskhorn_sequences.geojson \
--bbox=-83.1969970002756,42.3508899996029,-83.1869110001331,42.3583479999578

