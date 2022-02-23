FROM python:3.9
RUN apt-get update
RUN python -m pip install --upgrade pip
RUN apt-get install -y git ffmpeg libsm6 libxext6 imagemagick bc
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade --ignore-installed --no-cache-dir -r requirements.txt
WORKDIR /mnt
RUN pip install awscli
COPY . .
WORKDIR /mnt
