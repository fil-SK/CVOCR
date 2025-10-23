import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pytesseract

from contouring.detect_contours import detect_contours, visualise_contrours, simplify_contours, \
    simplify_contours_with_tolerance, approximate_polygon_contour
from image_related_ops.canny_algorithm import canny_edge_detection
from image_related_ops.gaussian_blur import calculate_sigma_from_kernel_size, create_gaussian_kernel, \
    perform_convolution
from image_related_ops.grayscale import convert_to_grayscale
from image_related_ops.load_image import load_image, save_current_image_state, display_resulting_image

IMAGE_DIR = "./test_images"
TARGET_IMAGE = "skoda_test.png"
DISPLAY_IMAGE = False

if __name__ == '__main__':

    # ------ STEP 0: Loading START ------
    print(f"Loading an image: {IMAGE_DIR}/{TARGET_IMAGE}")
    img_nparray = load_image(f"{IMAGE_DIR}/{TARGET_IMAGE}")         # Image is of shape (H,W,C)
    print(f"Original image shape: {img_nparray.shape}")
    # ------ STEP 0: Loading END ------


    # ------ STEP 1: Grayscale START ------
    gray_img_nparray = convert_to_grayscale(img_nparray)
    print(f"Grayscale image's shape: {gray_img_nparray.shape}")     # (H,W)
    if DISPLAY_IMAGE:
        display_resulting_image(gray_img_nparray)
    save_current_image_state(gray_img_nparray, "image", "1", "grayscale")
    # ------ STEP 1: Grayscale END ------


    # ------ STEP 2: Gaussian Blur START ------
    sigma = calculate_sigma_from_kernel_size(5)
    gaussian_kernel = create_gaussian_kernel(kernel_size=5, sigma=sigma)
    gaussian_blur_applied = perform_convolution(gray_img_nparray, gaussian_kernel)
    if DISPLAY_IMAGE:
        display_resulting_image(gaussian_blur_applied)
    save_current_image_state(gaussian_blur_applied, "image", "2", "gaussian_blur")
    # ------ STEP 2: Gaussian Blur END ------


    # ------ STEP 3: Canny edge detection algorithm START ------
    cannyfied_image = canny_edge_detection(gaussian_blur_applied, low_threshold=30, high_threshold=60)      # TODO: Play around with these values and check how it responds to
    if DISPLAY_IMAGE:
        display_resulting_image(cannyfied_image)
    save_current_image_state(cannyfied_image, "image", "3", "canny_edge_detection")
    # ------ STEP 3: Canny edge detection algorithm END ------


    # ------ STEP 4: Find contours START ------
    contours = detect_contours(cannyfied_image)
    visualise_contrours(cannyfied_image, contours, 4, "contours_colored")

    simplified_contours = simplify_contours(contours)
    if simplified_contours is not None:
        visualise_contrours(cannyfied_image, simplified_contours, 5, "simplified_contours_colored")

    # However, this implementation was too strict as it was expecting literal direction flip
    # In reality that is not the case, so we need to account for smaller degree changes, like 20 degrees e.g.
    simplified_contours_w_tolerance = simplify_contours_with_tolerance(contours, angle_tolerance=60)
    if simplified_contours_w_tolerance is not None:
        visualise_contrours(cannyfied_image, simplified_contours_w_tolerance, 5.1, "simplified_contours_tolerance_colored")

    # ------ STEP 4: Find contours END ------

    # ------ STEP 5: Contour sorting START ------

    dp_contours = approximate_polygon_contour(contours)
    #visualise_contrours(cannyfied_image, dp_contours, 6, "dr_contoured")

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


    # With cv2 implementation
    image = cv2.imread(f"{IMAGE_DIR}/{TARGET_IMAGE}")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to remove noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection (Canny) to highlight plate contours
    edges = cv2.Canny(blurred, 100, 200)

    # Find contours to locate the license plate
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours based on area (descending order)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    plate_contour = None
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the contour has 4 vertices (which may be a rectangle, typical for plates)
        if len(approx) == 4:
            plate_contour = approx
            break

    if plate_contour is not None:
        # Draw a bounding box around the detected license plate
        x, y, w, h = cv2.boundingRect(plate_contour)
        plate_image = gray[y:y + h, x:x + w]

        # Apply thresholding to binarize the plate area
        _, thresh = cv2.threshold(plate_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Perform OCR on the detected plate area
        plate_number = pytesseract.image_to_string(thresh, config='--psm 8')  # Treat it as a single word

        print(f"{plate_number.strip()}")
    else:
        print(f"License plate not detected")

    # ------ STEP 5: Contour sorting END ------

    # ------ STEP 6: Extract licence plate START ------

    # With cv2 implementation


    # My implementation

    # TODO: cv2.boundingRect(plate_contour)
    # TODO: cv2.threshold

    # ------ STEP 6: Extract licence plate END ------

    # ------ STEP 7: Perform OCR START ------

    # TODO: plate_number = pytesseract.image_to_string(thresh, config='--psm 8')  # Treat it as a single word
    #         return plate_number.strip()

    # ------ STEP 7: Perform OCR END ------