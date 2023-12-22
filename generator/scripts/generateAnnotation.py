import os
import pprint
import json
from xml.etree import ElementTree as ET

with open('config.json', 'r') as f:
    config = json.load(f)

def generateAnnotation(images_info, output_xml_dir):
    """
    Creates an XML annotation file that shows the positions of various
    items in a generated image.
    
    Parameters:
      images_info : array with image and location data
      
    """

    # Ensure the output directory exists
    if not os.path.exists(output_xml_dir):
        os.makedirs(output_xml_dir)
    
    if images_info:  # Check if images_info is not empty
        filename = images_info[0]["filename"]

    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = 'images'
    ET.SubElement(annotation, 'filename').text = filename  # Using the filename from images_info

    # Add size element
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(config['output']['width'])
    ET.SubElement(size, 'height').text = str(config['output']['height'])
    ET.SubElement(size, 'depth').text = '3'

    for image_info in images_info:  # Iterating over each dictionary in images_info
        object_elem = ET.SubElement(annotation, 'object')

        # Extracting info from the image_info dictionary
        ET.SubElement(object_elem, 'name').text = image_info["className"]
        ET.SubElement(object_elem, 'pose').text = 'Unspecified'
        ET.SubElement(object_elem, 'truncated').text = '0'
        ET.SubElement(object_elem, 'occluded').text = '0'
        ET.SubElement(object_elem, 'difficult').text = '0'

        bndbox = ET.SubElement(object_elem, 'bndbox')
        x_offset, y_offset = image_info["offset"]
        img_width, img_height = image_info["size"]

        ET.SubElement(bndbox, 'xmin').text = str(x_offset)
        ET.SubElement(bndbox, 'ymin').text = str(y_offset)
        ET.SubElement(bndbox, 'xmax').text = str(x_offset + img_width)
        ET.SubElement(bndbox, 'ymax').text = str(y_offset + img_height)

    # Constructing the full path to save the XML file
    savePath = os.path.join(output_xml_dir, filename + '.xml')  # Ensuring the filename has .xml extension
    print("Saving annotation to:", savePath)
    tree = ET.ElementTree(annotation)
    tree.write(savePath)

