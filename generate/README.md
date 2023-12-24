# scribble train - generator

Create tensor lite trainings sets from sheets of shapes.  (Created with macOS, but should work anywhere.)

To be used in conjunction with [this tutorial video](https://www.youtube.com/watch?v=kjuStyfl6yk) and [this collab notebook](https://colab.research.google.com/github/khanhlvg/tflite_raspberry_pi/blob/main/object_detection/Train_custom_model_tutorial.ipynb)

## Installation

SVG manipulation depends on [Inkscape](https://inkscape.org/). Once installed, make sure the executable is registered in config.json.

[TODO : Move cairo functionality over to Inkscape.]

`brew install cairo`

(If you run in to a "can't find cairo" error, you may need to run the following : )

`sudo cp /opt/homebrew/Cellar/cairo/{YOUR CAIRO VERSION}/lib/libcairo.2.dylib /usr/local/lib`

Then 

`pip3 install opencv-python et-xmlfile cairosvg`


## File Preparation

PNG shape sheets should be have a transparent background with space between the shapes.

SVG shape sheets should have all lines associated with a single shape grouped.


## Usage

Once you have prepared your files (I keep them in `input/sheets/filetype`) edit config.json to match your requirements.  Then first run `python init.py extract` to get individual shapes from the sheets, followed by `python init.py generate` to generate the training set.