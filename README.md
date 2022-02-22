# Mapillary image processing

Bunch of scripts to process and convert Mapillary spherical images into cube chunks for specific area.


## Buidl container

```sh
export MAPILLARY_ACCESS_TOKEN="MLY|..."
docker-compose build
```
### Download points from Mapillary

```sh
 python points.py \
    --output_point=data/Warrendale_points.geojson \
    --output_sequences=data/Warrendale_sequences.geojson \
    --bbox=-83.2469680005052,42.3289420003625,-83.2157740004676,42.3578449996934

```
### Simplify density of points

```
python simplify_points.py \
    --input_points=data/Warrendale_points_filter.geojson \
    --output_points=data/Warrendale_simplify.geojson
```



### Clip Pano images


docker-compose run mapimg bash
python main.py --bbox=-83.2263319287,42.3489816308,-83.2230326577,42.3507715447

### Or

docker run -v $PWD:/mnt/data/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN \
    -it devseed/mapimg:v1 python /app/main.py





mapimg

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
