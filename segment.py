### identifies + segments objects into b/w masks + pngs ###

import pixellib
from pixellib.torchbackend.instance import instanceSegmentation
import cv2
import os
import numpy as np

ins = instanceSegmentation()
ins.load_model("./models/pointrend_resnet50.pkl")

input_image_dir = "./frames/"
output_image_path = "./seg_frames/temp.jpg"
extracted_objects_dir = "./extracted_objs/"
masks_dir = "./masks/"

'''
segmask, output = ins.segmentImage(
    input_image_path,
    extract_segmented_objects=False,
    save_extracted_objects=False,
    show_bboxes=True,
    output_image_name=output_image_path
)

num_instances = segmask['masks'].shape[2]
'''

for j in range(290, 475):
    input_image_path = os.path.join(input_image_dir, f"{j}.jpg")

    segmask, output = ins.segmentImage(
        input_image_path,
        extract_segmented_objects=False,
        save_extracted_objects=False,
        show_bboxes=True,
        output_image_name=output_image_path
    )

    num_instances = segmask['masks'].shape[2]

    for i in range(1):
        mask = segmask['masks'][:, :, i]
        binary_mask = (mask * 255).astype(np.uint8)

        # jpg mask for background reconstruction
        height, width = binary_mask.shape
        black_bg = np.zeros((height, width), dtype=np.uint8)
        combined_mask = np.where(binary_mask == 255, 255, black_bg)
        cv2.imwrite(os.path.join(masks_dir, f"frame_{j}_mask.jpg"), combined_mask)

        # png segmented obj w/ transparent background
        original_image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
        if original_image.shape[2] == 3:
            original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2BGRA)

        alpha_channel = binary_mask
        b, g, r, a = cv2.split(original_image)
        a = alpha_channel
        image_rgba = cv2.merge([b, g, r, a])
      
        output_object_path = os.path.join(extracted_objects_dir, f"frame_{j}_obj_{i}.png")
        cv2.imwrite(output_object_path, image_rgba)

# cv2.imshow('img', output)
# cv2.imshow('mask', combined_mask)
# cv2.imshow('object', image_rgba)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
