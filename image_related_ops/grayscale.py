import numpy as np

# Coefficients to perform grayscaling - according to ITU-R BT.601 standard
R_COEFF = 0.299
G_COEFF = 0.587
B_COEFF = 0.114

def  convert_to_grayscale(img: np.ndarray) -> np.ndarray:
    """
    Converts RGB image to grayscale, using coefficients from ITU-R BT.601 standard. The function multiplies NumPy image
    representation with specified grayscale coefficients, and then casts the float result back into uint8 integers (0-255).

    Args:
        img (np.ndarray): RGB image to convert.

    Returns:
        np.ndarray: Grayscale representation of an image.
    """

    # Check if image is in RGB - has 3 channels
    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError("Image must have 3 channels. Image shape must be of (H,W,C).")

    print(f"\nTurning an image into grayscale.")
    grayscale_coefficients = np.array([R_COEFF, G_COEFF, B_COEFF])
    gray_img = np.dot(img, grayscale_coefficients)
    return gray_img.astype(np.uint8)                                    # np.dot produces float, so this will return the value to 0-255 int range