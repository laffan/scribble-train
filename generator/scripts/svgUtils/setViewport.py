import xml.etree.ElementTree as ET

def setViewport(svg_file, x_position, y_position, width, height):
    # Parse the SVG file
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Find the <svg> element. Assuming <svg> is the root
    svg_elem = root

    # Set the 'viewBox' attribute correctly
    view_box = [
        str(x_position - 5),  # min-x
        str(y_position - 5),  # min-y
        str(width+10),       # width of the viewport
        str(height+10)       # height of the viewport
    ]

    # Update the 'viewBox' attribute
    svg_elem.set('viewBox', ' '.join(view_box))

    # Write changes back to the file or a new file
    tree.write(svg_file)  # Overwrite the existing file or specify a new file name

