from PIL import Image
import numpy as np
import os

Image.MAX_IMAGE_PIXELS = 667423200

def mask_according_to_thermal(r_path, m_path, t_path, annotations_path, save_dir):
    # Load thermal image
    t_ = np.array(Image.open(t_path))
    
    if t_.shape[2] == 4:
        mask = np.all(t_ == np.array([0, 0, 0, 0]), axis=-1)
    else:
        # Create a mask with no effect if there are only 3 channels
        mask = np.zeros(t_.shape[:2], dtype=bool)

    # Load annotations
    annotations = []
    with open(annotations_path, 'r') as file:
        for line in file:
            annotations.append(line.strip().split())

    # Create a new annotations list with updated annotations
    new_annotations = []
    for annotation in annotations:
        x_center, y_center, width, height = map(float, annotation[1:])
        if not mask[int(y_center * t_.shape[0]), int(x_center * t_.shape[1])]:
            new_annotations.append(annotation)

    # Save the new annotations file
    new_annotations_path = os.path.join(save_dir, 'r_new.txt')
    with open(new_annotations_path, 'w') as file:
        for annotation in new_annotations:
            file.write(' '.join(annotation) + '\n')

    # Process images
    a = []
    for i, path in enumerate([r_path, m_path, t_path]):
        img = np.array(Image.open(path))
        
        if img.shape[2] == 4:
            img[mask] = np.array([0, 0, 0, 255])
        else:
            img = np.concatenate((img, 255 * np.ones((*img.shape[:2], 1), dtype=img.dtype)), axis=2)
            img[mask] = np.array([0, 0, 0, 255])
        
        img = Image.fromarray(img)
        img_path = os.path.join(save_dir, f'image_{i}.png')
        img.save(img_path)
        a.append(img_path)

    return a, new_annotations_path

# Example usage:
save_dir = 'C:\\Users\\user\\Documents'
r, m, t = mask_according_to_thermal(r_path=r'C:\Users\user\Desktop\Updated annotations-SET5\f5\r.png',
                                    m_path=r'C:\Users\user\Desktop\Updated annotations-SET5\f5\m.png',
                                    t_path=r'C:\Users\user\Desktop\Updated annotations-SET5\f5\t.png',
                                    annotations_path=r'C:\Users\user\Desktop\Updated annotations-SET5\f5\r.txt',
                                    save_dir=save_dir)

print(f'Saved images to {r}, {m}, {t}')

