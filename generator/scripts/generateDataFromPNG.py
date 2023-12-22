import os
import json
import random
from PIL import Image, ImageDraw, ImageOps
from scripts.generateAnnotation import generateAnnotation

with open('config.json', 'r') as f:
    config = json.load(f)

def generateDataFromPNG(categories, isValidationPass=False ):
  
    print("IS THIS THE FALIDATION PASS", isValidationPass)
    
    padding = config["output"]["padding"]  # Padding on all sides
    effective_width = config['output']['width'] - 2 * padding
    effective_height = config['output']['height'] - 2 * padding

    for img_num in range(config['output']['count']):
      
        images_info = []
        print ("Generating image", img_num)
        output_filename = f'img_{img_num}'
        # Create a white canvas
        canvas = Image.new('RGBA', (config['output']['width'], config['output']['height']), 'white')

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

            # Random position within the effective area
            x_max = max(config['output']['width'] - shape.width - padding, padding)
            y_max = max(config['output']['height'] - shape.height - padding, padding)

            # Ensure there's space to place the shape
            if x_max <= padding or y_max <= padding:
                continue  # Skip this shape if it can't be placed without overlap

            x_offset = random.randint(padding, x_max)
            y_offset = random.randint(padding, y_max)
            
            images_info.append(
                {
                 "className": category["className"], 
                 "filename" : output_filename, 
                 "offset": (x_offset, y_offset), 
                 "size": ( new_size[0], new_size[1])
                 }
                )
            
            # Overlay the shape onto the canvas
            canvas.paste(shape, (x_offset, y_offset), shape)


        # Figure out output directories
        validation_path = ("validate" if isValidationPass else "train")
        
        output_dir = os.path.join(config["paths"]["generated"], (validation_path if config["options"]["includeValidationSet"] else ""))
        
        output_img_dir = os.path.join(output_dir, ("images" if config["options"]["separateAnnotationFolder"] else ""))
        
        output_xml_dir = os.path.join(output_dir, ("annotations" if config["options"]["separateAnnotationFolder"] else ""))

        # Save the annotation
        generateAnnotation( images_info, output_xml_dir )

        # Ensure the output directory exists
        if not os.path.exists(output_img_dir):
            os.makedirs(output_img_dir)
        
        # Save the generated image
        canvas = canvas.convert("RGB")  # Convert to RGB if saving as JPEG
        canvas.save(os.path.join(output_img_dir, f'{output_filename}.jpg'))

