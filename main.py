import cv2
from PIL import Image

from contouring.detect_contours import detect_contours
from image_related_ops.canny_algorithm import canny_edge_detection
from image_related_ops.gaussian_blur import calculate_sigma_from_kernel_size, create_gaussian_kernel, \
    perform_convolution
from image_related_ops.grayscale import convert_to_grayscale
from image_related_ops.load_image import load_image, save_current_image_state

IMAGE_DIR = "./test_images"
TARGET_IMAGE = "mazda_one.png"

if __name__ == '__main__':

    # Load the image
    img_nparray = load_image(f"{IMAGE_DIR}/{TARGET_IMAGE}")
    print(f"Loaded image's shape: {img_nparray.shape}")


    # ------ STEP 1: Grayscale START ------

    # Turn image into grayscale
    gray_img_nparray = convert_to_grayscale(img_nparray)
    print(f"Grayscale image's shape: {gray_img_nparray.shape}")     # (H,W)

    # Display grayscale image to verify
    img_gray = Image.fromarray(gray_img_nparray)
    img_gray.show()
    save_current_image_state(gray_img_nparray, "image", "1", "grayscale")

    # ------ STEP 1: Grayscale END ------


    # ------ STEP 2: Gaussian Blur START ------

    sigma = calculate_sigma_from_kernel_size(5)
    gaussian_kernel = create_gaussian_kernel(kernel_size=5, sigma=sigma)
    gaussian_blur_applied = perform_convolution(gray_img_nparray, gaussian_kernel)

    # Display blurred image to verify
    blurred = Image.fromarray(gaussian_blur_applied)
    blurred.show()
    save_current_image_state(gaussian_blur_applied, "image", "2", "gaussian_blur")

    # ------ STEP 2: Gaussian Blur END ------


    # ------ STEP 3: Canny edge detection algorithm START ------

    cannyfied_image = canny_edge_detection(gaussian_blur_applied, low_threshold=30, high_threshold=60)      # TODO: Play around with these values and check how it responds to

    # Display image after Canny to verify
    cannyfied = Image.fromarray(cannyfied_image)
    cannyfied.show()
    save_current_image_state(cannyfied_image, "image", "3", "canny_edge_detection")

    # ------ STEP 3: Canny edge detection algorithm END ------


    # ------ STEP 4: Find contours START ------

    nodes = detect_contours(cannyfied_image)

    # ------ STEP 4: Find contours END ------