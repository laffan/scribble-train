import os
import json
from scripts.extractShapesFromPNG import extractShapesFromPNG
from scripts.extractShapesFromSVG import extractShapesFromSVG

with open('config.json', 'r') as f:
    config = json.load(f)

def extract( ):
    """
    Identifies correct directory and passes each images in it in to the
    correct extraction function.
    
    """
    
    inputDir = os.path.join(config['paths']['input'], config['formats']['input'])
    
    print( "Loading", inputDir )
    
    for filename in os.listdir( inputDir ):
        if filename.startswith('.'): #ignore invisible files
            continue
        if os.path.isfile(os.path.join(inputDir, filename)):
            filename = os.path.splitext(filename)[0]
            print (filename)
            if ( config['formats']['input'] == "png"):
              extractShapesFromPNG(filename)
            elif ( config['formats']['input'] == "svg"):
              extractShapesFromSVG(filename)
            else:
              print("Filetype not recognized.")
            
