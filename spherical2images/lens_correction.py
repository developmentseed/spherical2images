import lensfunpy
import cv2
from utils_images import correct_image
import os

cam_maker = "FUJIFILM"
cam_model = "X-T1"
lens_maker = "Samyang"
lens_model = "8mm f_2.8 UMC Fish-eye"
db = lensfunpy.Database()
camera = db.find_cameras(cam_maker, cam_model)[0]
lens = db.find_lenses(camera, lens_maker, lens_model)[0]

focal_length = 28.0
aperture = 1.4
distance = 10
# image
images = ["test_data/1_flat_right.jpeg", "test_data/1_flat_left.jpeg"]

for img_path in images:
    fixed_im = correct_image(img_path, camera, lens, focal_length, aperture, distance)
    img_path = os.path.splitext(img_path)[0]
    fixed_image_path = f"{img_path}_fixed.jpeg"
    cv2.imwrite(fixed_image_path, fixed_im)
    print(f"{img_path} -> {fixed_image_path}")
