from typing import Tuple

import numpy as np

# Used as a placeholder max value for one pixel
MAX_UINT8 = 255

# Angles used to check for the direction of the gradients
ANGLE_0_DEGREES = 0
ANGLE_45_DEGREES = 45
ANGLE_90_DEGREES = 90
ANGLE_135_DEGREES = 135

# Pixel values for the edges (on black background)
STRONG_EDGE_UINT8_VALUE = 255       # White
WEAK_EDGE_UINT8_VALUE = 80          # Gray
NO_EDGE_UINT8_VALUE = 0             # Black

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

def find_strength_and_orientation_of_edge(conv_img_x: np.ndarray, conv_img_y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculates the magnitude and orientation of edge on image convolved with Sobel kernel.

    Args:
        conv_img_x (np.ndarray): Image convolved with x-Sobel kernel.
        conv_img_y (np.ndarray): Image convolved with y-Sobel kernel.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Tuple representing Edge magnitude and orientation.
    """
    strength = np.hypot(conv_img_x, conv_img_y)                         # How strong the edge is at each pixel
    largest_gradient_value = strength.max()
    scaled_strength_values = strength / largest_gradient_value          # Scales into [0, 1] range
    strength_converted = scaled_strength_values * 255                   # Converted into [0, 255] range

    # Find the orientation of the edge
    orientation = np.arctan2(conv_img_x, conv_img_y)                    # How is edge oriented - where it points to

    return strength_converted, orientation


def check_for_direction_of_edge(angle: np.ndarray):
    # Approx. as 0 degrees - goes left-right; check above and below
    if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
        return (0, 1), (0, -1)

    # Approx. as 45 degrees
    elif (22.5 <= angle < 67.5):
        return (1, -1), (-1, 1)

    # Approx. as 90 degrees
    elif (67.5 <= angle < 112.5):
        return (1, 0), (-1, 0)

    # Approx. as 135 degrees
    elif (112.5 <= angle < 157.5):
        return (-1, -1), (1, 1)


def perform_nms(strength: np.ndarray, orientation: np.ndarray) -> np.ndarray:
    """
    Performs Non-Maximum Suppression (NMS) TODO

    Args:
        strength: TODO
        orientation: TODO
    Returns:
         (np.ndarray): TODO
    """
    img_magnitude_h, img_magnitude_w = strength.shape  # To iterate over every pixel
    nms_output_img_array = np.zeros((img_magnitude_h, img_magnitude_w),
                                dtype=np.float32)  # New image placeholder - will store the thinned edges after suppression


    # Convert radians to degrees
    angle = np.rad2deg(orientation)
    angle[angle < 0] += 180                 # Make angles positive


    # For each pixel(i, j) check on magnitude (strength) - on that pixel (so magnitude[i,j]), is that pixel strongest pixel along gradient orientation
    for i in range(1, img_magnitude_h - 1):
        for j in range(1, img_magnitude_w - 1):
            pixel_ahead = MAX_UINT8     # q
            pixel_before = MAX_UINT8    # r

            # Check for direction
            pixel_ahead_offset, pixel_before_offset = check_for_direction_of_edge(angle[i, j])

            # Calculate full index, by adding offset to i and j
            pixel_ahead_x, pixel_ahead_y = i + pixel_ahead_offset[0], j + pixel_ahead_offset[1]     # x-axis and y-axis for pixel_ahead
            pixel_before_x, pixel_before_y = i + pixel_before_offset[0], j + pixel_before_offset[1]

            # Get gradient magnitudes for those neighbors
            pixel_ahead = strength[pixel_ahead_x, pixel_ahead_y]
            pixel_before = strength[pixel_before_x, pixel_before_y]

            # Keep only local maxima
            # We want to keep the original viewed pixel (strength[i,j]) value, but only if he is stronger than his neighbors
            # Otherwise, we suppress the original viewed pixel value
            if (strength[i, j] >= pixel_ahead) and (strength[i, j] >= pixel_before):
                nms_output_img_array[i, j] = strength[i, j]
            else:
                nms_output_img_array[i, j] = 0

    return nms_output_img_array


def perform_double_threshold(nms_output_img_array: np.ndarray, low_threshold: int, high_threshold: int) -> np.ndarray:
    """
    After applying NMS, there might remain edges that are, essentially, noise.
    """

    filtered_nms_output = np.zeros_like(nms_output_img_array)       # Make NumPy array of same shape as NMS-outputed one. Initialize with 0

    # Find indices where rows and columns are above high threshold
    strong_x, strong_y = np.where(nms_output_img_array >= high_threshold)
    weak_x, weak_y = np.where((nms_output_img_array < high_threshold) & (nms_output_img_array >= low_threshold))

    filtered_nms_output[strong_x, strong_y] = STRONG_EDGE_UINT8_VALUE
    filtered_nms_output[weak_x, weak_y] = WEAK_EDGE_UINT8_VALUE

    return filtered_nms_output


def track_edge_by_hysteresis(double_threshold_output: np.ndarray, img_magnitude_h: int, img_magnitude_w: int):
    """
    Weak edges might touch strong or other weak edges. If it touches strong edge, probably belongs with it. Otherwise,
    it's noise and remove it.

    Args:
         TODO
    Returns:
        TODO
    """

    for i in range(1, img_magnitude_h - 1):
        for j in range(1, img_magnitude_w - 1):

            # Find weak pixel
            if double_threshold_output[i, j] == WEAK_EDGE_UINT8_VALUE:
                # Check if any of the 8 neighboring pixels are strong - if ANY is, keep that pixel value, otherwise, suppress it
                if (
                        (double_threshold_output[i - 1, j - 1] == STRONG_EDGE_UINT8_VALUE) or   # top left
                        (double_threshold_output[i, j - 1] == STRONG_EDGE_UINT8_VALUE) or       # top middle
                        (double_threshold_output[i + 1, j - 1] == STRONG_EDGE_UINT8_VALUE) or   # top right
                        (double_threshold_output[i + 1, j] == STRONG_EDGE_UINT8_VALUE) or       # mid right
                        (double_threshold_output[i + 1, j + 1] == STRONG_EDGE_UINT8_VALUE) or   # bot right
                        (double_threshold_output[i, j + 1] == STRONG_EDGE_UINT8_VALUE) or       # bot middle
                        (double_threshold_output[i - 1, j + 1] == STRONG_EDGE_UINT8_VALUE) or   # bot left
                        (double_threshold_output[i - 1, j] == STRONG_EDGE_UINT8_VALUE)          # mid left
                ):
                    # Keep that pixel - set it to strong
                    double_threshold_output[i, j] = STRONG_EDGE_UINT8_VALUE
                else:
                    # Suppress it
                    double_threshold_output[i, j] = NO_EDGE_UINT8_VALUE

    return double_threshold_output



def canny_edge_detection(blurred_img_ndarray: np.ndarray, low_threshold: int, high_threshold: int) -> np.ndarray:
    """
    Perform Canny Edge Detection algorithm to detect all edges in an image.

    Args:
        blurred_img_ndarray (np.ndarray): Image blurred with Gaussian Blur.

    Returns:
        (np.ndarray): Edge detection result.
    """
    print("Performing Canny Edge Detection...")

    # Prepare Sobel operators
    # Sobel_y inverses 1st and 3rd row, because, "on paper", y-axis goes upward, but in image processing, y-axis goes downward
    print("Preparing Sobel kernel...")
    sobel_x = np.array([[-1, 0, 1],
                              [-2, 0, 2],
                              [-1, 0, 1]], dtype=np.float32)

    sobel_y = np.array([[1, 2, 1],
                             [0, 0, 0],
                             [-1, -2, -1]], dtype=np.float32)


    # Perform convolution of an image with Sobel kernel
    print("Convolving image with Sobel kernel...")
    convolved_img_x = perform_convolution_image_sobel_filter(blurred_img_ndarray, sobel_x)
    convolved_img_y = perform_convolution_image_sobel_filter(blurred_img_ndarray, sobel_y)


    # Find the strength (magnitude) and orientation of the edge
    strength, orientation = find_strength_and_orientation_of_edge(convolved_img_x, convolved_img_y)

    ## Perform NMS
    print("Performing NMS...")
    nms_output_img_array = perform_nms(strength, orientation)

    # Perform double-threshold
    print("Performing Double Threshold...")
    double_threshold_output = perform_double_threshold(nms_output_img_array, low_threshold=low_threshold, high_threshold=high_threshold)

    # Perform hysteresis step
    print("Tracking edge by Hysteresis step...")
    img_magnitude_h, img_magnitude_w = strength.shape  # To iterate over every pixel
    hysteresis_output = track_edge_by_hysteresis(double_threshold_output, img_magnitude_h, img_magnitude_w)

    return hysteresis_output