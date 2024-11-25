### constructs clean background ###

import os
import numpy as np
import cv2

frames_dir = './frames/'
masks_dir = './masks/'
output_path = './reconstructed_background.jpg'

frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
mask_files = sorted([f for f in os.listdir(masks_dir) if f.endswith('.jpg')])

frames = []
masks = []

for frame_file, mask_file in zip(frame_files, mask_files):
    frame_path = os.path.join(frames_dir, frame_file)
    frame = cv2.imread(frame_path)
    frames.append(frame)

    mask_path = os.path.join(masks_dir, mask_file)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    _, mask = cv2.threshold(mask, 127, 1, cv2.THRESH_BINARY)
    masks.append(mask)

height, width, channels = frames[0].shape

# accumulate sum of bg pixel values over all frames
bg_sum = np.zeros((height, width, channels), dtype=np.float64)

# count no. of times pixel has been part of bg
bg_count = np.zeros((height, width), dtype=np.int32)

# track which pixels have been set in final bg
background = np.zeros((height, width, channels), dtype=np.uint8)
background_set = np.zeros((height, width), dtype=bool)

for frame, mask in zip(frames, masks):
    bg_mask = 1 - mask
    bg_mask_3d = np.repeat(bg_mask[:, :, np.newaxis], channels, axis=2)

    # v2: replace with first instance as bg pixel
    '''
    update_mask = (bg_mask == 1) & (~background_set)
    update_mask_3d = np.repeat(update_mask[:, :, np.newaxis], channels, axis=2)
    background[update_mask_3d] = frame[update_mask_3d]
    background_set[update_mask] = True
    '''

    # sum values of pixels not covered by mask
    bg_sum += frame * bg_mask_3d
    bg_count += bg_mask

non_zero_mask = bg_count > 0
bg_count_safe = bg_count.copy()
bg_count_safe[bg_count_safe == 0] = 1

# v1: compute average (divide total summed value of pixel by no. times counted as bg)
background = (bg_sum / bg_count_safe[..., np.newaxis]).astype(np.uint8)
background[~non_zero_mask] = 0

cv2.imwrite(output_path, background)
cv2.imshow('background', background)
cv2.waitKey(0)
cv2.destroyAllWindows()
