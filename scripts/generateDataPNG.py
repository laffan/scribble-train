from PIL import Image, ImageDraw, ImageOps
import os
import random

def generateDataPNG(categories, generated_count, generated_width, generated_height):
    outputDir = "output/generated"
    # Ensure the output directory exists
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    padding = 100  # Padding on all sides
    effective_width = generated_width - 2 * padding
    effective_height = generated_width - 2 * padding

    for img_num in range(generated_count):
        # Create a white canvas
        canvas = Image.new('RGBA', (generated_width, generated_height), 'white')

        # Decide how many shapes to use in this image (3 to 10)
        num_shapes = random.randint(3, 6)

        for _ in range(num_shapes):
            # Randomly select a category and an image from this category
            category = random.choice(categories)
            image_path = random.choice(category['images'])
            try:
                shape = Image.open(image_path).convert('RGBA')
            except IOError:
                print(f"Warning: Unable to load image {image_path}")
                continue  # Skip to the next shape

            # Randomly scale the shape
            scale_factor = random.uniform(1, 3)  # Scale from A to B.
            new_size = (int(shape.width * scale_factor), int(shape.height * scale_factor))
            shape = shape.resize(new_size, Image.Resampling.LANCZOS)

            # Check if shape fits within the effective area
            if shape.width > effective_width or shape.height > effective_height:
                continue  # Skip this shape if it doesn't fit

            # Random rotation
            angle = random.randint(0, 360)
            shape = shape.rotate(angle, expand=True)

            # Random position within the effective area
            x_max = max(generated_width - shape.width - padding, padding)
            y_max = max(generated_height - shape.height - padding, padding)

            # Ensure there's space to place the shape
            if x_max <= padding or y_max <= padding:
                continue  # Skip this shape if it can't be placed without overlap

            x_offset = random.randint(padding, x_max)
            y_offset = random.randint(padding, y_max)
            
            # Overlay the shape onto the canvas
            canvas.paste(shape, (x_offset, y_offset), shape)

        # Save the generated image
        canvas = canvas.convert("RGB")  # Convert to RGB if saving as JPEG
        canvas.save(os.path.join(outputDir, f'img_{img_num}.jpg'))

# Example usage
# categories = [...] # Your categories data
# generateData(categories, 'path_to_generated_data_directory', 30, 800, 600)
