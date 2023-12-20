import os
import xml.etree.ElementTree as ET

def isolateShapesSVG(sheetDirectory, shapesDirectory, filename):
  
    # For now we're just using the file name *as* the category
    category=filename
    
    # Load the image
    tree = ET.parse(os.path.join(sheetDirectory, filename + ".svg"))
    root = tree.getroot()

    if not os.path.exists(shapesDirectory):
        os.makedirs(shapesDirectory)

    shape_count = 0

    for element in root:
        if element.tag.endswith('path') or element.tag.endswith('g'):
          
            # Create a new SVG tree for each top-level path or group
            new_svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")
            new_svg.append(element)

            # Create the directory if it doesn't exist
            if not os.path.exists(os.path.join(shapesDirectory, filename)):
                os.makedirs(os.path.join(shapesDirectory, filename))
                
            # Write to file
            output_path = os.path.join(shapesDirectory, filename,  f'shape_{shape_count}.svg')
            with open(output_path, 'wb') as file:
                file.write(ET.tostring(new_svg))

            shape_count += 1

    return shape_count