import os 
import json 
from scripts.generateDataFromPNG import generateDataFromPNG
from scripts.generateDataFromSVG import generateDataFromSVG

with open('config.json', 'r') as f:
    config = json.load(f)

def selectGenerate( categories, isValidationPass=False  ): 
    if ( config["formats"]["input"] == "png"):
        generateDataFromPNG(categories, isValidationPass)
    else:
        generateDataFromSVG(categories, isValidationPass)


def generate( ):
    """
    Loops through all folders in the input directory and passes them in to
    the appropriate generateData function.
    """
    categories = []
    sourceDir = os.path.join(config["paths"]["shapes"], config["formats"]["input"])
    
    # Loop through each directory in the shapes Directory
    for folder_name in os.listdir(sourceDir):

        # Ignore invisibles
        if folder_name.startswith('.'):
            continue
          
        folder_path = os.path.join(sourceDir, folder_name)
        
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
                'className': folder_name,
                'images': images
            })

    # If we're creating a validaiton set as well, do that here.
    
    if config["options"]["includeValidationSet"] :
      for i in range(2):
        if (i == 0 ):       
          selectGenerate( categories )
        if (i == 1 ):       
          selectGenerate( categories, True )
    else :      
      selectGenerate( categories )
    
