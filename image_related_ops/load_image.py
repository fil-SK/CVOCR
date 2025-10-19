from pathlib import Path
from typing import Union

import numpy as np
from PIL import Image

PathLike = Union[str, Path]

def load_image(image_path : str) -> np.ndarray:
    """
    Loads image from the path, and returns ndarray
    """
    print(f"Loading {image_path}")
    img = (Image.open(image_path).convert("RGB"))   # ensures 3 channels
    img.show()

    return np.array(img)