from PIL import Image

Image.MAX_IMAGE_PIXELS = 667423200

def make_white_background_transparent(image_path, output_path):
    # Load the image
    image = Image.open(image_path).convert("RGBA")
    
    # Get the data of the image
    data = image.getdata()
    
    new_data = []
    for item in data:
        # Change all white (also shades of whites)
        # (255, 255, 255) to (0, 0, 0, 0)
        if item[:3] == (255, 255, 255):
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    
    # Update image data
    image.putdata(new_data)
    
    # Save the image with transparency
    image.save(output_path, "PNG")

# Example usage:
t_path = r'C:\Users\user\Desktop\Updated annotations-SET5\f5\t.png'
output_path = r'C:\Users\user\Desktop\Updated annotations-SET5\f5\t_transparent.png'
make_white_background_transparent(t_path, output_path)
print(f"Saved the image with transparent background to {output_path}")
