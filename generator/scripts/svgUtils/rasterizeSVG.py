import cairosvg
import xml.etree.ElementTree as ET

def rasterizeSVG(svg_path, img_output_path):
  
    # Hideous workaround because I can't figure out how to move paths 
    # to origin. Instead I'm just rasterizing an enormous canvas and 
    # then removing transparent pixels 
  
    try:
        # Parse the SVG file
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # Set a large viewBox
        root.set('viewBox', '0 0 4000 4000')

        # Save the modified SVG temporarily
        temp_svg_path = 'temp.svg'
        tree.write(temp_svg_path)
        print( "rasterizing", svg_path)
        
        # Rasterize the SVG to PNG
        cairosvg.svg2png(url=temp_svg_path, write_to=img_output_path)

    except Exception as e:
        print(f"An error occurred: {e}")
      