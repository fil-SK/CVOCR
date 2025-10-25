from contouring.detect_contours import detect_contours, visualise_contrours, simplify_contours, \
    simplify_contours_with_tolerance, approximate_polygon_contour
from external_src.gfg_impl import gfg_implementation
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
    img_nparray = load_image(f"{IMAGE_DIR}/{TARGET_IMAGE}")         # Image is of shape (H,W,C)
    print(f"Original image shape: {img_nparray.shape}")
    # ------ STEP 0: Loading END ------


    # ------ STEP 1: Grayscale START ------
    gray_img_nparray = convert_to_grayscale(img_nparray)
    print(f"Grayscale image's shape: {gray_img_nparray.shape}")     # (H,W)
    if DISPLAY_IMAGE:
        display_resulting_image(gray_img_nparray)
    save_current_image_state(gray_img_nparray, TARGET_IMAGE, "1", "grayscale")
    # ------ STEP 1: Grayscale END ------


    # ------ STEP 2: Gaussian Blur START ------
    sigma = calculate_sigma_from_kernel_size(5)
    gaussian_kernel = create_gaussian_kernel(kernel_size=5, sigma=sigma)
    gaussian_blur_applied = perform_convolution(gray_img_nparray, gaussian_kernel)
    if DISPLAY_IMAGE:
        display_resulting_image(gaussian_blur_applied)
    save_current_image_state(gaussian_blur_applied, TARGET_IMAGE, "2", "gaussian_blur")
    # ------ STEP 2: Gaussian Blur END ------


    # ------ STEP 3: Canny edge detection algorithm START ------
    cannyfied_image = canny_edge_detection(TARGET_IMAGE, gaussian_blur_applied, low_threshold=30, high_threshold=60)      # TODO: Play around with these values and check how it responds to
    if DISPLAY_IMAGE:
        display_resulting_image(cannyfied_image)
    save_current_image_state(cannyfied_image, TARGET_IMAGE, "3", "canny_edge_detection")
    # ------ STEP 3: Canny edge detection algorithm END ------


    # ------ STEP 4: Find contours START ------
    contours = detect_contours(cannyfied_image)
    visualise_contrours(cannyfied_image, contours, TARGET_IMAGE, 4, "contours_colored")

    simplified_contours = simplify_contours(contours)
    if simplified_contours is not None:
        visualise_contrours(cannyfied_image, simplified_contours, TARGET_IMAGE,  5, "simplified_contours_colored")

    # However, this implementation was too strict as it was expecting literal direction flip
    # In reality that is not the case, so we need to account for smaller degree changes, like 20 degrees e.g.
    simplified_contours_w_tolerance = simplify_contours_with_tolerance(contours, angle_tolerance=60)
    if simplified_contours_w_tolerance is not None:
        visualise_contrours(cannyfied_image, simplified_contours_w_tolerance, TARGET_IMAGE,  5.1, "simplified_contours_tolerance_colored")
    # ------ STEP 4: Find contours END ------


    # ------ STEP 5: Line simplification DP-alg START ------
    dp_contours = approximate_polygon_contour(contours)
    #visualise_contrours(cannyfied_image, dp_contours, TARGET_IMAGE,  6, "dr_contoured")
    # ------ STEP 5: Line simplification DP-alg END ------


    # ------ STEP 6: Original implementer code START ------
    gfg_implementation(IMAGE_DIR, TARGET_IMAGE)
    # ------ STEP 6: Original implementer code END ------
