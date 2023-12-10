import os
import re
import random
import cairosvg
from PIL import Image
from xml.etree import ElementTree as ET

def scale_svg(input_svg_path, output_svg_path, scale_factor):
    try:
        # Parse the SVG file
        tree = ET.parse(input_svg_path)
        root = tree.getroot()

        # Scale path 'd' attributes
        for path_element in root.findall('.//{http://www.w3.org/2000/svg}path'):
            d_attr = path_element.get('d')

            # Scale the coordinates in the 'd' attribute
            scaled_d = scale_path_d(d_attr, scale_factor)
            path_element.set('d', scaled_d)

        tree.write(output_svg_path)
    except Exception as e:
        print(f"An error occurred: {e}")

def scale_path_d(d_attr, scale_factor):
    # This is a simple implementation and might need to be expanded
    # based on the path commands used in your SVGs
    numbers = map(float, re.findall(r"[-+]?\d*\.?\d+|\d+", d_attr))
    scaled_numbers = [str(n * scale_factor) for n in numbers]
    return re.sub(r"[-+]?\d*\.?\d+|\d+", lambda match: scaled_numbers.pop(0), d_attr, len(scaled_numbers))

def rasterize_svg(svg_path, png_output_path):
    try:
        # Parse the SVG file
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # Set a large viewBox
        root.set('viewBox', '0 0 5000 5000')

        # Save the modified SVG temporarily
        temp_svg_path = 'temp.svg'
        tree.write(temp_svg_path)
        print( "rasterizing", svg_path)
        # Rasterize the SVG to PNG
        cairosvg.svg2png(url=temp_svg_path, write_to=png_output_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        
def set_svg_stroke(svg_path, stroke_width=2, stroke_color="black"):
    try:
        # Parse SVG for path elements and update stroke attributes
        tree = ET.parse(svg_path)

        svg_root = tree.getroot()
        for path_element in svg_root.iter('{http://www.w3.org/2000/svg}path'):
            path_element.set('stroke-width', str(stroke_width))
            path_element.set('stroke', stroke_color)
            path_element.set('fill', 'none')
            
        # Save modified SVG
        ET.ElementTree(svg_root).write(svg_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        
def combine_images(output_png_path, images_info):
    # Assuming images_info is a list of tuples: (image_path, position, rotation)
    base_image = Image.new('RGBA', (800, 600), 'white')  # Adjust size as needed

    for img_info in images_info:
        img_path, position, rotation = img_info
        with Image.open(img_path) as img:
            img = img.rotate(rotation, expand=True)
            base_image.paste(img, position, img)

    base_image.save(output_png_path)


def trim_transparency(png_path):
    try:
        img = Image.open(png_path)
        bbox = img.getbbox()

        if bbox:
            img = img.crop(bbox)
            img.save(png_path)
    except Exception as e:
        print(f"An error occurred: {e}")
  
        
def generateDataSVG(categories, generated_count, generated_width, generated_height):
    outputDir = "output/generated"
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    padding = 100
    effective_width = generated_width - 2 * padding
    effective_height = generated_height - 2 * padding

    for img_num in range(generated_count):
        images_info = []  # To store info about each image to combine

        for _ in range(random.randint(3, 6)):  # Decide how many shapes to use in this image
            category = random.choice(categories)
            svg_path = random.choice(category['images'])  # Select a random SVG path

            scaled_svg_path = os.path.join(outputDir, f'scaled_{img_num}_{_}.svg')
            png_path = os.path.join(outputDir, f'rasterized_{img_num}_{_}.png')

            scale_factor = random.uniform(.5, 3)  # Randomly scale the shape
            try:
                scale_svg(svg_path, scaled_svg_path, scale_factor) # scale
                set_svg_stroke( scaled_svg_path ) # set stroke and color
                rasterize_svg(scaled_svg_path, png_path) # rasterize svg
                os.remove(scaled_svg_path) # delete scaled svg
                trim_transparency(png_path) # Remove transparent pixels

                # # Random rotation and position
                # angle = random.randint(0, 360)
                # x_offset = random.randint(padding, effective_width)
                # y_offset = random.randint(padding, effective_height)

                # images_info.append((png_path, (x_offset, y_offset), angle))
                
            except Exception as e:
                print(f"Error processing SVG {svg_path}: {e}")
                continue

        # output_png_path = os.path.join(outputDir, f'img_{img_num}.png')
        # combine_images(output_png_path, images_info)
