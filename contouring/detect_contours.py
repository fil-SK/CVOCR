import numpy as np

from image_related_ops.canny_algorithm import STRONG_EDGE_UINT8_VALUE


def check_for_neighboring_pixels(cannyfied_image: np.ndarray, pixel_x: int, pixel_y: int,
                                 list_of_pixels_to_check:  list[tuple[int, int]], checked_pixels: np.ndarray):
    """
    TODO

    Args:
         TODO
    Returns:
        TODO
    """

    img_h, img_w = cannyfied_image.shape

    # ------- Check for the top row -------

    # If there is top row and if top-left pixel is WHITE and not previously checked ---> Add it to list of pixels to be checked
    # if not pixel_x > 0 and pixel_y > 0 ---> might be that top row doesn't exist, if checked pixel is in top row of image
    if pixel_x > 0 and pixel_y > 0 and cannyfied_image[pixel_y - 1, pixel_x - 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y - 1, pixel_x - 1]:
        list_of_pixels_to_check.append((pixel_y - 1, pixel_x - 1))

    # Top-middle pixel
    if pixel_x > 0 and pixel_y > 0 and cannyfied_image[pixel_y - 1, pixel_x] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y - 1, pixel_x]:
        list_of_pixels_to_check.append((pixel_y - 1, pixel_x))

    # Top-right pixel
    if pixel_x > 0 and pixel_y > 0 and cannyfied_image[pixel_y - 1, pixel_x + 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y - 1, pixel_x + 1]:
        list_of_pixels_to_check.append((pixel_y - 1, pixel_x + 1))


    # ------ Check for the middle row ------

    # Middle-left pixel
    # if not pixel_x > 0 ---> Checked pixel is in the most middle-left part
    if pixel_x > 0 and cannyfied_image[pixel_y, pixel_x - 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y, pixel_x - 1]:
        list_of_pixels_to_check.append((pixel_y, pixel_x - 1))

    # Middle-right pixel
    # if not pixel_x < img_w ---> Checked pixel is in the most middle-right part
    if pixel_x < img_w - 1 and cannyfied_image[pixel_y, pixel_x + 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y, pixel_x + 1]:
        list_of_pixels_to_check.append((pixel_y, pixel_x + 1))


    # ------ Check for the bottom row ------

    # Bottom-left pixel
    if pixel_y < img_h - 1 and pixel_x > 0 and cannyfied_image[pixel_y + 1, pixel_x - 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y + 1, pixel_x - 1]:
        list_of_pixels_to_check.append((pixel_y + 1, pixel_x - 1))

    # Bottom-mid pixel
    if pixel_y < img_h - 1 and cannyfied_image[pixel_y + 1, pixel_x] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y + 1, pixel_x]:
        list_of_pixels_to_check.append((pixel_y + 1, pixel_x))

    # Bottom-right pixel
    if pixel_y < img_h - 1 and pixel_x < img_w - 1 and cannyfied_image[pixel_y + 1, pixel_x + 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[
        pixel_y + 1, pixel_x + 1]:
        list_of_pixels_to_check.append((pixel_y + 1, pixel_x + 1))


def detect_contours(cannyfied_image: np.ndarray) -> np.ndarray:
    """
    Loops through all pixels and finds connected white pixels that form a contour.
    Args:
        TODO
    Returns:
        TODO
    """

    contours = []
    checked_pixels = np.zeros_like(cannyfied_image, dtype=bool)     # Placeholder for same shaped NumPy array. Each pixel has value 0 - initially not checked

    img_h, img_w = cannyfied_image.shape

    # Check every pixel
    for i in range(img_h):      # y
        for j in range(img_w):  # x

            # If pixel is white and wasn't checked before
            if cannyfied_image[i, j] == 255 and not checked_pixels[i, j]:

                # Start new contour
                contour = []
                pixel_to_check = (i, j)
                list_of_pixels_to_check = [pixel_to_check]      # This pixel is unchecked. Add it to list of those that needs to be checked


                # Perform DFS search for unchecked pixels - until you reach a checked one
                while list_of_pixels_to_check:
                    pixel_x, pixel_y = list_of_pixels_to_check.pop()

                    # If we already visited it - skip and go to next pixel
                    if checked_pixels[pixel_x, pixel_y]:
                        continue

                    # If we didn't visit it - now we did, set to 1
                    checked_pixels[pixel_x, pixel_y] = 1
                    contour.append((pixel_x, pixel_y))      # We found the pixel we checked, therefore we completed the circle - contour

                    # For this pixel check it's neighboring pixels and add them if not checked already
                    check_for_neighboring_pixels(cannyfied_image, pixel_x, pixel_y, list_of_pixels_to_check, checked_pixels)


                # Once list of pixels that should be checked is empty - we are finished
                # Add all collected points to the main list of contours
                contours.append(contour)