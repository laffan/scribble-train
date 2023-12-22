from PIL import Image

def trimTransparency(png_path):
    try:
        img = Image.open(png_path)
        bbox = img.getbbox()

        if bbox:
            img = img.crop(bbox)
            img.save(png_path)
    except Exception as e:
        print(f"An error occurred: {e}")

