import xml.etree.ElementTree as ET

def setSVGStroke(svg_path, stroke_width=2, stroke_color="black"):
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
        