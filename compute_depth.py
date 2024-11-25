### compute real-world depth of object in each frame ###

import pixellib
from pixellib.torchbackend.instance import instanceSegmentation
import cv2
import os
import numpy as np
import csv
import matplotlib.pyplot as plt

''' convert pixel coordinates to spherical angles '''
def calculate_spherical_angles(u, v, W, H):
    theta = 2 * np.pi * (u / W - 0.5)
    phi = np.pi * (0.5 - v / H)
    return theta, phi

''' calculate distance from pixel to camera using direction rays '''
def calculate_distance(u, v, W, H, camera_height):
    theta, phi = calculate_spherical_angles(u, v, W, H)

    # convert to direction vector
    dx = np.cos(phi) * np.sin(theta)
    dy = np.sin(phi)
    dz = np.cos(phi) * np.cos(theta)

    if dy == 0:
        return None

    '''
    P(t) = C + t * d
         = (0, h, 0) + t * (dx, dy, dz)
         = (t * dx, h + t * dy, t * dz)
    t = -h / dy
    '''
    t = -camera_height / dy
    return t

''' detect x-coord of pixel that sets lower bound of bbox '''
def detect_bottom_x_pos(mask, bbox):
    xmin, ymin, xmax, ymax = bbox

    # crop mask to bbox
    cropped_mask = mask[ymin:ymax, xmin:xmax]

    lower_bound = cropped_mask[-1, :]
    mask_x_positions = np.where(lower_bound == 1)[0]

    if len(mask_x_positions) == 0:
        return 0

    # shift x pos by left bound
    x_pos = mask_x_positions[0] + xmin
    return x_pos

''' calculate distance from object to camera for each frame '''
def process_frames(input_image_dir, output_file, camera_height):
    ins = instanceSegmentation()
    ins.load_model("./models/pointrend_resnet50.pkl")

    distances = []

    for j in range(290, 475):
        input_image_path = os.path.join(input_image_dir, f"{j}.jpg")

        segmask, output = ins.segmentImage(
            input_image_path,
            extract_segmented_objects=False,
            save_extracted_objects=False,
            show_bboxes=True,
        )

        for i in range(1):
            xmin, ymin, xmax, ymax = segmask['boxes'][i]
            mask = segmask['masks'][:, :, i]

            x_pos = detect_bottom_x_pos(mask, (xmin, ymin, xmax, ymax))

            u = x_pos
            v = ymax

            image = cv2.imread(input_image_path)
            H, W, _ = image.shape

            distance = calculate_distance(u, v, W, H, camera_height)

            # save pixel coordinates for unity script usage
            distances.append(distance)

    # print(results)
    np.savetxt(output_file, distances, delimiter=',')

if __name__ == "__main__":
    input_image_dir = './frames/'
    output_file = './distances.csv'
    camera_height = 10.0

    process_frames(input_image_dir, output_file, camera_height)
