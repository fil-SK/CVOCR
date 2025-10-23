import os
import numpy as np
from PIL import Image

IMAGE_STATES_DIR = "image_states"


def load_image(image_path : str) -> np.ndarray:
    """
    Loads an image from the specified path, and returns ndarray image representation.

    Args:
        image_path (str): Path to the image.

    Returns:
        (np.ndarray): NumPy image representation.
    """
    print(f"Loading {image_path}")
    img = (Image.open(image_path).convert("RGB"))   # ensures 3 channels, in this order: (H, W, C)
    #img.show()

    return np.array(img)


def save_current_image_state(img_nparray: np.ndarray, img_name: str, step: str, action:str) -> None:
    """
    Saves current state of the image. This is used to track and verify the entire process, enabling the user to
    pass the current NumPy array representation of the image, and to have such image transformed into PNG file
    and saved on the system.

    Args:
         img_nparray (np.ndarray): NumPy image representation.
         img_name (str): Original name of an image.
         step (str): Current step in the execution pipeline.
         action (str): Current action of the execution pipeline.

    Returns:
        (None)
    """
    print(f"Saving image, step {step}: {action}")

    # Ensure the output folder exists
    os.makedirs(IMAGE_STATES_DIR, exist_ok=True)

    # Form image output name
    filename = f"{img_name}_{step}_{action}.png"
    path = os.path.join(IMAGE_STATES_DIR, filename)

    # Convert NumPy array to PIL image
    # Detect if grayscale (2D) or RGB (3D)
    if img_nparray.ndim == 2:
        img = Image.fromarray(img_nparray.astype('uint8'), mode='L')
    elif img_nparray.ndim == 3:
        img = Image.fromarray(img_nparray.astype('uint8'), mode='RGB')
    else:
        raise ValueError("Cannot save image in this unsupported image shape.")

    # Save as PNG (lossless)
    img.save(path)
    print(f"Saved image on: {path}")