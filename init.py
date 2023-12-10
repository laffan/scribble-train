import os
import sys
from scripts.isolateShapesPNG import isolateShapesPNG
from scripts.isolateShapesSVG import isolateShapesSVG
from scripts.generateDataPNG import generateDataPNG
from scripts.generateDataSVG import generateDataSVG

generated_count = 3
generated_width = 1000
generated_height = 720

def extract( type ):
    sheetDirectory = f"src/shape-sheets/{type}"
    shapesDirectory=f"output/shapes/{type}"
    for filename in os.listdir(sheetDirectory):
        if filename.startswith('.'):
            continue
        if os.path.isfile(os.path.join(sheetDirectory, filename)):
            filename = os.path.splitext(filename)[0]
            if ( type == "png"):
              isolateShapesPNG(sheetDirectory, shapesDirectory, filename)
            else:
              isolateShapesSVG(sheetDirectory, shapesDirectory, filename)
            
                
def generate( type ):
    categories = []
    shapesDirectory=f"output/shapes/{type}"
    # Loop through each directory in the shapesDirectory
    for folder_name in os.listdir(shapesDirectory):

        # Ignore invisibles
        if folder_name.startswith('.'):
            continue
        folder_path = os.path.join(shapesDirectory, folder_name)
        # Check if it's a directory
        if os.path.isdir(folder_path):
            images = []

            # Loop through each file in the directory
            for filename in os.listdir(folder_path):
                # Ignore invisibles
                if filename.startswith('.'):
                    continue

                file_path = os.path.join(folder_path, filename)
                
                # If it's a file, append.
                if os.path.isfile(file_path):
                    images.append(file_path)

            # Add the category and its images to the categories list
            categories.append({
                'category': folder_name,
                'images': images
            })

    print(categories)
    if ( type == "png"):
      generateDataPNG(categories, generated_count, generated_width, generated_height)
    else:
      generateDataSVG(categories, generated_count, generated_width, generated_height)


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "extract-png":
            extract('png')
        elif arg == "extract-svg":
            extract('svg')
        elif arg == "generate-png":
            generate('png')
        elif arg == "generate-svg":
            generate('svg')
        else:
            print("Invalid argument.")
    else:
        print("No argument provided.")

if __name__ == "__main__":
    main()
