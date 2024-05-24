import os
import random
import shutil
import yaml

# Input and output directories
input_dir = 'C:\\Users\\user\\Documents\\elies\\initial data\\channelsum'
output_image_dir = 'C:\\Users\\user\\Desktop\\yolo\\images'
output_label_dir = 'C:\\Users\\user\\Desktop\\yolo\\labels'
yaml_file_path = 'C:\\Users\\user\\Desktop\\yolo\\data.yaml'

# Ensure output directories exist
for output_dir in [output_image_dir, output_label_dir]:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# List of classes
classes = ['healthy', 'minor damage', 'medium damage', 'high damage']

# Create data.yaml
data_yaml = {
    'train': '../images/train',
    'val': '../images/test',
    'nc': len(classes),
    'names': classes
}

with open(yaml_file_path, 'w') as yaml_file:
    yaml.dump(data_yaml, yaml_file)

# Create train and test directories
for dataset_type in ['train', 'val']:
    dataset_image_dir = os.path.join(output_image_dir, dataset_type)
    dataset_label_dir = os.path.join(output_label_dir, dataset_type)
    
    if not os.path.exists(dataset_image_dir):
        os.makedirs(dataset_image_dir)
    
    if not os.path.exists(dataset_label_dir):
        os.makedirs(dataset_label_dir)

# Move files randomly into train and test directories
for filename in os.listdir(input_dir):
    if filename.endswith('.png'):
        # Randomly select train or test dataset
        dataset_type = 'train' if random.random() < 0.8 else 'val'
        
        # Move image
        shutil.move(os.path.join(input_dir, filename), os.path.join(output_image_dir, dataset_type, filename))
        
        # Create corresponding label file
        label_filename = filename.replace('.png', '.txt')
        open(os.path.join(output_label_dir, dataset_type, label_filename), 'a').close()
