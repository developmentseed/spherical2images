import sys
import json
import unittest
import glob
from spherical2images.utils_images import process_image

sys.path.append("..")


class Test_clip_images(unittest.TestCase):
    def test_clip_images(self):
        """Test clip images"""
        with open("tests/fixtures/points.geojson", "r", encoding="utf8") as f:
            features = json.load(f)["features"][:4]
        image_path = "tests/fixtures/data"
        output = process_image(features, image_path, 1024, "left,right")
        images_left = len(glob.glob(f"{image_path}/*/*_left.jpg"))
        images_right = len(glob.glob(f"{image_path}/*/*_right.jpg"))
        self.assertEqual(images_left, 4)
        self.assertEqual(images_right, 4)
