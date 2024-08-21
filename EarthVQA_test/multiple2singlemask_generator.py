import os
import numpy as np
from skimage.io import imread, imsave
from collections import OrderedDict
from tqdm import tqdm  # For progress bar

# Define the color map and select the class
COLOR_MAP = OrderedDict(
    Background=(255, 255, 255),
    Building=(255, 0, 0),
    Road=(255, 255, 0),
    Water=(0, 0, 255),
    Barren=(159, 129, 183),
    Forest=(0, 255, 0),
    Agricultural=(255, 195, 128),
    Playground=(165, 0, 165),
    Pond=(0, 185, 246),
)

# Set paths
input_mask_dir = 'dataset/Train/masks_png_v2'
output_mask_dir = 'dataset/Train/water_masks_png'

# Create the output directory if it doesn't exist
os.makedirs(output_mask_dir, exist_ok=True)

# Define the class you want to extract
class_to_extract = 'Water'
class_index = 4 # Since you mentioned Water's value is 4, no need to subtract 1

# Process each mask image
for mask_filename in tqdm(os.listdir(input_mask_dir)):
    if mask_filename.endswith(('.png', '.jpg', '.tif')):
        # Read the multi-class mask
        mask_path = os.path.join(input_mask_dir, mask_filename)
        mask = imread(mask_path).astype(np.int64)
        
        # Create a binary mask where the selected class is 1 and others are 0
        binary_mask = (mask == class_index).astype(np.uint8)
        
        # Scale binary mask to 255 for PNG format
        binary_mask = binary_mask * 255
        
        # Save the binary mask as a PNG image
        output_path = os.path.join(output_mask_dir, mask_filename)
        imsave(output_path, binary_mask)



