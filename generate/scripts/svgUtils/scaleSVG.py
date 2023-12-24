import json
import random
import re
import xml.etree.ElementTree as ET

with open('config.json', 'r') as f:
    config = json.load(f)

import re

def scalePath(d_attr, scale_factor):
    # Extract numbers from the d attribute of the path
    numbers = map(float, re.findall(r"[-+]?\d*\.?\d+|\d+", d_attr))

    # Scale numbers and format to two decimal places
    scaled_numbers = ["{:.2f}".format(n * scale_factor) for n in numbers]

    # Replace old numbers in the path with scaled values
    return re.sub(r"[-+]?\d*\.?\d+|\d+", lambda match: scaled_numbers.pop(0), d_attr, len(scaled_numbers))

    
def scaleSVG(input_svg, output_svg):
    scale_factor = random.uniform(config["output"]["scale"][0], config["output"]["scale"][1])  # Randomly scale the shape
    max_width = config["output"]["width"]
    max_height = config["output"]["height"]
    
    try:
        # Parse the SVG file
        tree = ET.parse(input_svg)
        root = tree.getroot()

        # Scale path 'd' attributes
        for path_element in root.findall('.//{http://www.w3.org/2000/svg}path'):
            d_attr = path_element.get('d')

            # Scale the coordinates in the 'd' attribute
            scaled_d = scalePath(d_attr, scale_factor)
            path_element.set('d', scaled_d)

        tree.write(output_svg)
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
