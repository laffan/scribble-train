import xml.etree.ElementTree as ET
from scripts.svgUtils.scalePath import scalePath

def scaleSVG(input_svg_path, output_svg_path, scale_factor):
    try:
        # Parse the SVG file
        tree = ET.parse(input_svg_path)
        root = tree.getroot()

        # Scale path 'd' attributes
        for path_element in root.findall('.//{http://www.w3.org/2000/svg}path'):
            d_attr = path_element.get('d')

            # Scale the coordinates in the 'd' attribute
            scaled_d = scalePath(d_attr, scale_factor)
            path_element.set('d', scaled_d)

        tree.write(output_svg_path)
    except Exception as e:
        print(f"An error occurred: {e}")
