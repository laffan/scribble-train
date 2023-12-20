from PIL import Image
import os

def reencode_images(directory):
    for subdir, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
                filepath = os.path.join(subdir, filename)
                try:
                    with Image.open(filepath) as img:
                        img.save(filepath, "JPEG")
                    print(f"Re-encoded: {filepath}")
                except Exception as e:
                    print(f"Failed to re-encode {filepath}: {e}")

reencode_images('shapes')