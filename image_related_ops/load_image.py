import numpy as np
from PIL import Image

def load_image(image_path : str) -> np.ndarray:
    """
    Loads image from the path, and returns ndarray image representation.

    Args:
        image_path (str): Path to the image.

    Returns:
        (np.ndarray): NumPy image representation.
    """
    print(f"Loading {image_path}")
    img = (Image.open(image_path).convert("RGB"))   # ensures 3 channels
    img.show()

    return np.array(img)