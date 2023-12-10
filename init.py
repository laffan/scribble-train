import os
import sys
from scripts.isolateShapes import isolateShapes
from scripts.generateData import generateData

sheetDirectory = "src/shape-sheets"  # Replace with your directory
shapesDirectory = "output/shapes"  # Replace with your directory
generatedDataDirectory = "output/generated"  # Replace with your directory
generated_width = 1000
generated_height = 720

def extract():
    for filename in os.listdir(sheetDirectory):
        print(filename)
        if os.path.isfile(os.path.join(sheetDirectory, filename)):
            filename = os.path.splitext(filename)[0]
            parts = filename.split('--')
            if len(parts) == 2:
                name, category = parts
                isolateShapes(sheetDirectory, shapesDirectory, filename, category)
                
def generate():
    categories = []

    # Loop through each directory in the shapesDirectory
    for folder_name in os.listdir(shapesDirectory):
        folder_path = os.path.join(shapesDirectory, folder_name)
        
        # Check if it's a directory
        if os.path.isdir(folder_path):
            images = []

            # Loop through each file in the directory
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                # Check if it's a file
                if os.path.isfile(file_path):
                    images.append(file_path)

            # Add the category and its images to the categories list
            categories.append({
                'category': folder_name,
                'images': images
            })

    generateData( categories, generatedDataDirectory, 30, generated_width, generated_height )

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "extract":
            extract()
        elif arg == "generate":
            generate()
        else:
            print("Invalid argument. Use 'extract' or 'generate'.")
    else:
        print("No argument provided. Use 'extract' or 'generate'.")

if __name__ == "__main__":
    main()
