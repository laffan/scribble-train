import os
import json
import re
import random
from PIL import Image
from scripts.generateAnnotation import generateAnnotation
from scripts.svgUtils.scaleSVG import scaleSVG 
from scripts.svgUtils.setSVGStroke import setSVGStroke 
from scripts.svgUtils.rasterizeSVG import rasterizeSVG 
from scripts.pngUtils.trimTransparency import trimTransparency 

with open('config.json', 'r') as f:
    config = json.load(f)
        
def generateDataFromSVG(categories, isValidationPass=False ):

    
    if not os.path.exists(config["paths"]["generated"]):
        os.makedirs(config["paths"]["generated"])

    padding = config["output"]["padding"]
    effective_width = config["output"]["width"] - 2 * config["output"]["padding"]
    effective_height = config["output"]["height"] - 2 * config["output"]["padding"]

    for img_num in range(config["output"]["count"]):
        tempFileList = []
        print ("Generating image", img_num)
        output_filename = f'img_{img_num}'
        images_info = []  # To store info about each image to combine

        for _ in range(random.randint(3, 6)):  # Decide how many shapes to use in this image
            selectedCategory = random.choice(categories)
            svg_path = random.choice(selectedCategory['images'])  # Select a random SVG path

            canvas = Image.new('RGBA', (config['output']['width'], config['output']['height']), 'white')

            scaled_svg_path = os.path.join(config["paths"]["generated"], f'scaled_{img_num}_{_}.svg')
            png_path = os.path.join(config["paths"]["generated"], f'rasterized_{img_num}_{_}.png')
            
            tempFileList.append(scaled_svg_path)
            tempFileList.append(png_path)

            scale_factor = random.uniform(.5, 3)  # Randomly scale the shape
            try:
                scaleSVG(svg_path, scaled_svg_path, scale_factor) # scale
                setSVGStroke( scaled_svg_path ) # set stroke and color
                rasterizeSVG(scaled_svg_path, png_path) # rasterize svg
                trimTransparency(png_path) # Remove transparent pixels

                # # Random rotation and position
                x_offset = random.randint(padding, effective_width)
                y_offset = random.randint(padding, effective_height)
                width, height = Image.open(png_path).size

                # images_info.append(( category_name, png_path, (x_offset, y_offset), ( width, height)))

                images_info.append(
                {
                 "className": selectedCategory["className"], 
                 "filename" : output_filename, 
                 "offset": (x_offset, y_offset), 
                 "size": ( width, height )
                 }
                )
                
                # Combine images
                try:
                  shape = Image.open(png_path).convert('RGBA')
                except IOError:
                    print(f"Warning: Unable to load image {png_path}")
                    continue  # Skip to the next shape
              
                # Overlay the shape onto the canvas
                canvas.paste(shape, (x_offset, y_offset), shape)
              
            except Exception as e:
                print(f"Error processing SVG {svg_path}: {e}")
                continue

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

        # Remove temp files
        for file_path in tempFileList:
            try:
                os.remove(file_path)
            except FileNotFoundError:
                print(f"File {file_path} was not found")
            except Exception as e:
                print(f"An error occurred: {e}")