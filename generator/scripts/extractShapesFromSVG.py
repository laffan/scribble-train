import os
import json
import xml.etree.ElementTree as ET

with open('config.json', 'r') as f:
    config = json.load(f)

def extractShapesFromSVG( filename ):
    """
    Exports top level groups to a folder that has the name of the original file.

    """
        
    # Load the image
    tree = ET.parse(os.path.join(config['paths']['input'], "svg", filename + ".svg"))
    root = tree.getroot()

    shapesDir = os.path.join(config['paths']['shapes'], "svg")
    if not os.path.exists(shapesDir):
        os.makedirs(shapesDir)

    shape_count = 0

    for element in root:
        if element.tag.endswith('path') or element.tag.endswith('g'):
          
            # Create a new SVG tree for each top-level path or group
            new_svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")
            new_svg.append(element)

            # Create the directory if it doesn't exist
            if not os.path.exists(os.path.join(shapesDir, filename)):
                os.makedirs(os.path.join(shapesDir, filename))
                
            # Write to file
            output_path = os.path.join(shapesDir, filename,  f'shape_{shape_count}.svg')
            with open(output_path, 'wb') as file:
                file.write(ET.tostring(new_svg))

            shape_count += 1

    return shape_count