FROM python:3.9
RUN apt -y install git
RUN python -m pip install --upgrade pip
RUN apt-get update
RUN apt-get install  -y ffmpeg libsm6 libxext6 imagemagick
RUN pip install opencv-python mercantile mapbox_vector_tile vt2geojson requests
COPY sphericalpano2cube.sh /usr/bin/sphericalpano2cube
WORKDIR /mnt
COPY . .
