# Spherical to simple side images

Bunch of scripts to process and convert Mapillary spherical images into cube imagen and then into simple images for specific area in Mapillary API.

## Build container

```sh
export MAPILLARY_ACCESS_TOKEN="MLY|..."
docker-compose build
```

### Download points from Mapillary into geojson file

```sh
docker run -v $PWD:/mnt/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed/spherical2images:v1 \
    get_mapillary_points \
        --output_file_point=data/Warrendale_points.geojson \
        --output_file_sequence=data/Warrendale_sequences.geojson \
        --bbox=-83.2469680005052,42.3289420003625,-83.2157740004676,42.3578449996934
```

### Simplify density of points

```sh
docker run -v $PWD:/mnt/ -it developmentseed/spherical2images:v1 \
    simplify_points \
        --input_points=data/Warrendale_points_filter.geojson \
        --output_points=data/Warrendale_simplify.geojson
```

### Clip Pano images into left an right side

```sh
docker run -v $PWD:/mnt/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed/spherical2images:v1 \
    clip_mapillary_pano \
        --input_file_points=data/Warrendale_points_filter.geojson \
        --image_clip_size=1024 \
        --output_file_points=data/Warrendale_points_fixed.geojson \
        --output_images_path=data/ \
        --cube_sides=right,left
```

_Note_
For converting spherical-pano image to cubemap image, we are using [py360convert](https://github.com/sunset1995/py360convert):

## Example:

- Mapillary spherical-pano image:

![](img/380223760052524.jpg)

- Cube:

|               Front                |                Back                |
| :--------------------------------: | :--------------------------------: |
| ![](img/380223760052524_front.jpg) | ![](/img/380223760052524_back.jpg) |

|               Left                |               Right                |
| :-------------------------------: | :--------------------------------: |
| ![](img/380223760052524_left.jpg) | ![](img/380223760052524_right.jpg) |

|               Under                |               Over                |
| :--------------------------------: | :-------------------------------: |
| ![](img/380223760052524_under.jpg) | ![](img/380223760052524_over.jpg) |
