# scribble train - generator

Create tensor lite trainings sets from sheets of shapes.  (Created with macOS, but should work anywhere.)

To be used in conjunction with [this tutorial video](https://www.youtube.com/watch?v=kjuStyfl6yk) and [this collab notebook](https://colab.research.google.com/github/khanhlvg/tflite_raspberry_pi/blob/main/object_detection/Train_custom_model_tutorial.ipynb)

## Installation

SVG manipulation depends on Inkscape. Getting it up and running on macOS 




`brew install cairo`

(If you run in to a "can't find cairo" error, you may need to run the following : )

`sudo cp /opt/homebrew/Cellar/cairo/{YOUR CAIRO VERSION}/lib/libcairo.2.dylib /usr/local/lib`

Then 

`pip3 install opencv-python et-xmlfile cairosvg`


## Currently

- 🚨🚨🚨 Adding SVG support, but *keep the raster version*. Will be useful for other projects.