import numpy as np

KERNEL_5x5_SIZE = 5
SIGMA_X = 0

def calculate_sigma_from_kernel_size(kernel_size: int) -> float:
    """
    Calculate the sigma value from kernel size, according to the formula OpenCV uses.

    Args:
        kernel_size (int): Kernel size. For 5x5 kernel, kernel_size is 5.

    Returns:
        float: Calculated sigma value.
    """
    sigma = ((kernel_size - 1) * 0.5 - 1) * 0.3 + 0.8
    return sigma


def create_gaussian_kernel(kernel_size:int, sigma:float) -> np.ndarray:
    """
    Create a gaussian kernel from the given kernel size and perform the Gaussian 2D formula on the kernel values,
    using specified kernel size and passed sigma value, in order to form teh Gaussian kernel.

    Args:
        kernel_size (int): Kernel size. For 5x5 kernel, kernel_size is 5.
        sigma (float): Sigma value. Calculated using the OpenCV formula.
    """

    # Generate Kernel matrix
    half_width = kernel_size // 2     # For kernel=5, will return 5 // 2 = 2
    x, y = np.mgrid[-half_width:half_width + 1, -half_width:half_width + 1]     # Makes a nxn matrix, with values -2,-1,0,1,2

    # Prepare Gaussian formula
    normal_const = 1 / (2.0 * np.pi * sigma**2)     # This part is used for normalization (total area under the curve = 1); Not necessary, sometimes omitted
    gaussian_2d_formula = normal_const * np.exp(- ( (x**2 + y**2) / (2.0 * sigma**2) ) )

    normalized_result = gaussian_2d_formula / gaussian_2d_formula.sum()
    return normalized_result


def perform_convolution(image_nparray: np.ndarray, gaussian_kernel: np.ndarray) -> np.ndarray:
    """
    Performs the 2D convolution on (grayscale) image and generated Gaussian kernel.

    Args:
        image_nparray (np.ndarray): Grayscale image, in NumPy format.
        gaussian_kernel (np.ndarray): Generated Gaussian kernel, in NumPy format.

    Returns:
        np.ndarray: Image after convolution - finalized Gaussian blur operation.
    """

    # Image and kernel shapes
    img_h, img_w = image_nparray.shape
    k_h, k_w = gaussian_kernel.shape

    # Pad the image to handle borders
    pad_h = k_h // 2
    pad_w = k_w // 2
    padded_img = np.pad(image_nparray, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')

    # Placeholder variable for output image
    output = np.zeros_like(image_nparray, dtype=float)

    # Perform convolution
    for i in range(img_h):
        for j in range(img_w):
            # Extract region of interest
            region = padded_img[i:i + k_h, j:j + k_w]
            # Multiply elementwise and sum
            output[i, j] = np.sum(region * gaussian_kernel)

    return output