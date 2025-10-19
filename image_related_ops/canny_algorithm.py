import numpy as np


def perform_convolution_image_sobel_filter(img_nparray: np.ndarray, sobel_kernel: np.ndarray) -> np.ndarray:
    """
    Perform convolution of image with Sobel operator. Convolution is done with regard to specific dimension
    of Sobel operator passed.

    Args:
        img_nparray: Image with Gaussian Blur applied.
        sobel_kernel: Sobel kernel to be applied.

    Returns:
        np.ndarray: Image with Sobel convolution applied.
    """

    # Image and kernel shapes
    img_h, img_w = img_nparray.shape
    sobel_h, sobel_w = sobel_kernel.shape

    # Pad the image to handle borders
    pad_h = sobel_h // 2
    pad_w = sobel_w // 2
    padded_img = np.pad(img_nparray, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0) # pads with zeros

    # Placeholder variable for output image
    output = np.zeros_like(img_nparray, dtype=float)

    # Perform convolution
    for i in range(img_h):
        for j in range(img_w):
            # Extract region of interest
            region = padded_img[i:i + sobel_h, j:j + sobel_w]
            # Multiply elementwise and sum
            output[i, j] = np.sum(region * sobel_kernel)

    return output



def canny_edge_detection(blurred_img_ndarray: np.ndarray) -> np.ndarray:
    """
    Perform Canny Edge Detection algorithm to detect all edges in an image.

    Args:
        blurred_img_ndarray (np.ndarray): Image blurred with Gaussian Blur.

    Returns:
        (np.ndarray): Edge detection result.
    """

    # Prepare Sobel operators
    # Sobel_y inverses 1st and 3rd row, because, "on paper", y-axis goes upward, but in image processing, y-axis goes downward
    sobel_x = np.array([[-1, 0, 1],
                              [-2, 0, 2],
                              [-1, 0, 1]], dtype=np.float32)

    sobel_y = np.array([[1, 2, 1],
                             [0, 0, 0],
                             [-1, -2, -1]], dtype=np.float32)


    # Perform convolution of an image with Sobel kernel
    convolved_img_x = perform_convolution_image_sobel_filter(blurred_img_ndarray, sobel_x)
    convolved_img_y = perform_convolution_image_sobel_filter(blurred_img_ndarray, sobel_y)


    # Find the strength (magnitude) of the edge
    strength = np.hypot(convolved_img_x, convolved_img_y)
    largest_gradient_value = strength.max()
    scaled_strength_values = strength / largest_gradient_value      # Scales into [0, 1] range
    strength_converted = scaled_strength_values * 255               # Converted into [0, 255] range

    # Find the orientation of the edge
    orientation = np.arctan2(convolved_img_y, convolved_img_x)