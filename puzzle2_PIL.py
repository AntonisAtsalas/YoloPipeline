import os
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = 487423200

# Load the large images
r_image = np.array(Image.open('C:\\Users\\user\\Documents\\elies\\initial data\\r_resized.png'))
m_image = np.array(Image.open('C:\\Users\\user\\Documents\\elies\\initial data\\m_resized.png'))
t_image = np.array(Image.open('C:\\Users\\user\\Documents\\elies\\initial data\\t_resized.png'))

# Load the annotations
with open('C:\\Users\\user\\Documents\\elies\\initial data\\r.txt', 'r') as r_annotations_file:
    r_annotations = r_annotations_file.readlines()

# Define the size of the smaller images
small_image_size = 2000

# Define the stride for cropping
stride = small_image_size

# Initialize the index for the smaller images
index = 0

# Iterate over the large image and crop smaller portions
for y in range(0, r_image.shape[0], stride):
    for x in range(0, r_image.shape[1], stride):
        # Calculate the coordinates for cropping
        x_start = x
        y_start = y
        x_end = min(x + small_image_size, r_image.shape[1])
        y_end = min(y + small_image_size, r_image.shape[0])

        # Crop the images
        r_small_image = r_image[y_start:y_end, x_start:x_end]
        m_small_image = m_image[y_start:y_end, x_start:x_end]
        t_small_image = t_image[y_start:y_end, x_start:x_end]

        # Write the relevant annotations to the new annotation files
        annotation_file_path = f'C:\\Users\\user\\Documents\\elies\\initial data\\new\\results_{index}.txt'
        with open(annotation_file_path, 'w') as small_annotation_file:
            for r_annotation in r_annotations:
                # Parse the annotation
                class_id, x_center, y_center, width, height = map(float, r_annotation.split())
                class_id = int(class_id)

                # Convert normalized coordinates to absolute coordinates
                x_center *= r_image.shape[1]
                y_center *= r_image.shape[0]

                # Check if the annotation is within the cropped portion
                if x_start <= x_center <= x_end and y_start <= y_center <= y_end:
                    # Adjust the coordinates relative to the cropped portion
                    x_center -= x_start
                    y_center -= y_start

                    # Normalize the coordinates relative to the cropped portion
                    x_center_norm = x_center / small_image_size
                    y_center_norm = y_center / small_image_size
                    width_norm = width * r_image.shape[1] / small_image_size
                    height_norm = height * r_image.shape[0] / small_image_size

                    # Write the adjusted annotation to the small annotation file
                    small_annotation_file.write(f'{class_id} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

        # Check if the annotation file is empty
        if os.path.getsize(annotation_file_path) > 0:
            # Save the cropped images
            Image.fromarray(r_small_image).save(f'C:\\Users\\user\\Documents\\elies\\initial data\\new\\r_{index}.png')
            Image.fromarray(m_small_image).save(f'C:\\Users\\user\\Documents\\elies\\initial data\\new\\m_{index}.png')
            Image.fromarray(t_small_image).save(f'C:\\Users\\user\\Documents\\elies\\initial data\\new\\t_{index}.png')

            # Increment the index for the smaller images
            index += 1
