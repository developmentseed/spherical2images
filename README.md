# Mapillary spherical to cube images

This a simple script to convert Mapillary spherical images into cube chunks for specific area.

- Excute the script

```sh
export MAPILLARY_ACCESS_TOKEN="MLY|..."
docker-compose build
docker-compose run spherical2cube bash
python main.py --bbox=-83.2263319287,42.3489816308,-83.2230326577,42.3507715447

### Or

docker run -v $PWD:/mnt/data/ -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN \
    -it devseed/spherical2cube:v1 python /app/main.py
```

spherical2cube

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
