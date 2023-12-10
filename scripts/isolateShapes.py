import cv2
import os
import numpy as np

def isolateShapes(sheetDirectory, shapesDirectory, filename, category):
  
    # Load the image
    original_image = cv2.imread(os.path.join(sheetDirectory, filename + ".png"), cv2.IMREAD_UNCHANGED)

    # Convert to grayscale
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGRA2GRAY)

    # Find all contours in the grayscale image
    contours, _ = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Function to create a transparent image with the same size as the original
    def create_blank(width, height, color=(0, 0, 0, 0)):
        image = np.zeros((height, width, 4), np.uint8)
        image[:] = color
        return image

    CONTAINER_DIR = os.path.join(shapesDirectory, category)

    # Create the directory if it doesn't exist
    if not os.path.exists(CONTAINER_DIR):
        os.makedirs(CONTAINER_DIR)

    # Iterate through contours and isolate each shape
    for i, contour in enumerate(contours):
        # Create a mask for the current contour
        mask = np.zeros_like(gray_image)
        cv2.drawContours(mask, [contour], -1, 255, -1)

        # Create a bounding box around the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Crop the original image using the bounding box
        cropped = original_image[y:y+h, x:x+w]
        mask_cropped = mask[y:y+h, x:x+w]

        # Create a blank image and draw the cropped shape on it
        blank_image = create_blank(width=w, height=h)
        blank_image[mask_cropped == 255] = cropped[mask_cropped == 255]

        # Save the shape as a new image
        output_filename = f"{CONTAINER_DIR}/{filename}_{i}.png"
        cv2.imwrite(output_filename, blank_image)

    # Return the number of shapes found
    return len(contours)
