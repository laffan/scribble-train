import subprocess
import json
import xml.etree.ElementTree as ET
from scripts.svgUtils.setViewport import setViewport

with open('config.json', 'r') as f:
    config = json.load(f)

def moveSVGToOrigin(input_svg):
  
    # Parse the SVG file
    tree = ET.parse(input_svg)
    root = tree.getroot()
    root.set('viewBox', '0 0 0 0')
    tree.write(input_svg)


    inkscape_path = config["paths"]["inkscape"]
    print ("Scaling viewport for ", input_svg)
    
    command = [
        inkscape_path,
        '--actions',
        f"select-all;query-all",
        input_svg,
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    resultTrimmed = result.stdout.strip().split('\n')[0]

    # Split the resultTrimmed by commas
    svgName, x, y, width, height = resultTrimmed.split(',')

    # Convert x, y, width, and height to integers
    x_pos = int(float(x))
    y_pos = int(float(y))
    width = int(float(width))
    height = int(float(height))    

    setViewport(input_svg, x_pos, y_pos, width, height )
