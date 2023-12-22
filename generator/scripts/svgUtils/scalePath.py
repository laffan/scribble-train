import re

def scalePath(d_attr, scale_factor):
    # This is a simple implementation and might need to be expanded
    # based on the path commands used in your SVGs
    numbers = map(float, re.findall(r"[-+]?\d*\.?\d+|\d+", d_attr))
    scaled_numbers = [str(n * scale_factor) for n in numbers]
    return re.sub(r"[-+]?\d*\.?\d+|\d+", lambda match: scaled_numbers.pop(0), d_attr, len(scaled_numbers))
