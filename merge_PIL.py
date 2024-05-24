import os
from PIL import Image
import numpy as np

# Input and output directories
r_input_dir = r'C:\Users\user\Documents\elies\initial data\decolorize'
m_input_dir = r'C:\Users\user\Documents\elies\initial data\new'
t_input_dir = r'C:\Users\user\Documents\elies\initial data\new'
output_dir = r'C:\Users\user\Documents\elies\initial data\channelsum'

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over files in the r_input_dir
for r_filename in os.listdir(r_input_dir):
    if r_filename.endswith('.png'):
        # Extract index from filename
        index = r_filename.split('_')[1].split('.')[0]
        
        # Load r_image
        r_image = Image.open(os.path.join(r_input_dir, r_filename))
        r_band = np.array(r_image)[:, :, 0:1]  # Extract the decolorized band (all bands are the same)
        
        # Load m_image
        m_filename = f'm_{index}.png'
        m_image = Image.open(os.path.join(m_input_dir, m_filename))
        m_band = np.array(m_image)[:, :, 2:3]  # Extract multispectral band
        
        # Load t_image
        t_filename = f't_{index}.png'
        t_image = Image.open(os.path.join(t_input_dir, t_filename))
        t_band = np.array(t_image)[:, :, :1]  # Extract thermal band 
        
        # Merge the three bands into one image
        merged_image = np.concatenate((r_band, m_band, t_band), axis=2)
        
        # Convert the merged image back to PIL format and save
        merged_image_pil = Image.fromarray(merged_image, mode='RGB')
        output_filename = f'results_{index}.png'
        merged_image_pil.save(os.path.join(output_dir, output_filename))

print("Images processed and saved successfully.")
