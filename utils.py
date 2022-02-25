import cv2
from PIL import Image
from smart_open import open
import pathlib


def build_sequence(points):
    # Build sequence lines and save
    sequences = {}
    points_sorted = sorted(points, key=lambda item: int(item["properties"]["captured_at"]))
    for point in points_sorted:
        sequence_id = str(point["properties"]["sequence_id"])
        if sequence_id not in sequences.keys():
            sequences[sequence_id] = {
                "type": "Feature",
                "properties": {"sequence_id": sequence_id},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [point["geometry"]["coordinates"]],
                },
            }
        else:
            sequences[sequence_id]["geometry"]["coordinates"].append(
                point["geometry"]["coordinates"]
            )

    return list(sequences.values())


def cubemap_splitter(
    img_file_cubemap, image_clip_size, sequence_id, image_id, output_images_path, cube_sides
):
    img = cv2.imread(img_file_cubemap)
    img_height = img.shape[0]
    img_width = img.shape[1]
    r = img_width - img_height
    h = w = image_clip_size
    horizontal_chunks = 4
    vertical_chunks = 3
    index_dict = {
        "1,0": "top",
        "0,1": "left",
        "1,1": "front",
        "2,1": "right",
        "3,1": "back",
        "1,2": "bottom",
    }
    sides = cube_sides.split(",")
    for x in range(0, horizontal_chunks):
        for y in range(0, vertical_chunks):
            index = f"{x},{y}"
            if index in index_dict.keys() and index_dict[index] in sides:
                crop_img = img[y * r : y * r + h, x * r : x * r + w]
                imageRGB = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
                img_ = Image.fromarray(imageRGB, mode="RGB")
                chunk_img_path = (
                    f"{output_images_path}/{sequence_id}/{image_id}_{index_dict[index]}.jpg"
                )
                with open(chunk_img_path, "wb") as sfile:
                    img_.save(sfile)
                    print(f"Saving...{chunk_img_path}")
