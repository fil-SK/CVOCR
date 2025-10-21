import os
import cv2
import math
import numpy as np
from image_related_ops.load_image import IMAGE_STATES_DIR
from image_related_ops.canny_algorithm import STRONG_EDGE_UINT8_VALUE


def check_if_pixel_within_image(pixel_x:int ,pixel_y:int, img_h:int, img_w:int)->bool:
    if pixel_x < img_w - 1 and pixel_y < img_h - 1:
        return True
    else:
        return False

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
    if pixel_x > 0 and pixel_y > 0 and check_if_pixel_within_image(pixel_x, pixel_y, img_h, img_w) and cannyfied_image[pixel_y - 1, pixel_x - 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y - 1, pixel_x - 1]:
        list_of_pixels_to_check.append((pixel_y - 1, pixel_x - 1))

    # Top-middle pixel
    if pixel_x > 0 and pixel_y > 0 and check_if_pixel_within_image(pixel_x, pixel_y, img_h, img_w) and cannyfied_image[pixel_y - 1, pixel_x] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y - 1, pixel_x]:
        list_of_pixels_to_check.append((pixel_y - 1, pixel_x))

    # Top-right pixel
    if pixel_x > 0 and pixel_y > 0 and check_if_pixel_within_image(pixel_x, pixel_y, img_h, img_w) and cannyfied_image[pixel_y - 1, pixel_x + 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y - 1, pixel_x + 1]:
        list_of_pixels_to_check.append((pixel_y - 1, pixel_x + 1))


    # ------ Check for the middle row ------

    # Middle-left pixel
    # if not pixel_x > 0 ---> Checked pixel is in the most middle-left part
    if pixel_x > 0 and check_if_pixel_within_image(pixel_x, pixel_y, img_h, img_w) and cannyfied_image[pixel_y, pixel_x - 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y, pixel_x - 1]:
        list_of_pixels_to_check.append((pixel_y, pixel_x - 1))

    # Middle-right pixel
    # if not pixel_x < img_w ---> Checked pixel is in the most middle-right part
    if pixel_x < img_w - 1 and check_if_pixel_within_image(pixel_x, pixel_y, img_h, img_w) and cannyfied_image[pixel_y, pixel_x + 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y, pixel_x + 1]:
        list_of_pixels_to_check.append((pixel_y, pixel_x + 1))


    # ------ Check for the bottom row ------

    # Bottom-left pixel
    if pixel_y < img_h - 1 and pixel_x > 0 and check_if_pixel_within_image(pixel_x, pixel_y, img_h, img_w) and cannyfied_image[pixel_y + 1, pixel_x - 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y + 1, pixel_x - 1]:
        list_of_pixels_to_check.append((pixel_y + 1, pixel_x - 1))

    # Bottom-mid pixel
    if pixel_y < img_h - 1 and check_if_pixel_within_image(pixel_x, pixel_y, img_h, img_w) and cannyfied_image[pixel_y + 1, pixel_x] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[pixel_y + 1, pixel_x]:
        list_of_pixels_to_check.append((pixel_y + 1, pixel_x))

    # Bottom-right pixel
    if pixel_y < img_h - 1 and pixel_x < img_w - 1 and check_if_pixel_within_image(pixel_x, pixel_y, img_h, img_w) and cannyfied_image[pixel_y + 1, pixel_x + 1] == STRONG_EDGE_UINT8_VALUE and not checked_pixels[
        pixel_y + 1, pixel_x + 1]:
        list_of_pixels_to_check.append((pixel_y + 1, pixel_x + 1))


def detect_contours(cannyfied_image: np.ndarray) -> list[list[tuple[int, int]]]:
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
                contour : list[tuple[int, int]] = []
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

    return contours


def visualise_contrours(cannyfied_image: np.ndarray, contours: list[list[tuple[int, int]]], step, name) -> None:
    """
    TODO
    """

    img_color = cv2.cvtColor(cannyfied_image, cv2.COLOR_GRAY2BGR)
    for contour_list in contours:
        for x, y in contour_list:
            cv2.circle(img_color, (y, x), 1, (0, 255, 0), -1)       # TODO: Why (y,x) ???

    cv2.imshow("Contours", img_color)
    cv2.waitKey(0)

    # Save contoured image
    path = os.path.join(IMAGE_STATES_DIR, f"image_step_{step}_{name}.png")
    cv2.imwrite(path, img_color)



def simplify_contours(list_of_contours: list[list[tuple[int, int]]]) -> list[list[tuple[int, int]]] | None:
    """
    For each point, compare direction coming in and going out. If the direction changes it’s a corner so keep it.
    Else it’s a straight line, so remove it.
    """

    print("Simplifying the contours")
    simplified_contours = []

    for contour in list_of_contours:
        # We need at least 4 points to make a rectangle contour, if not present, we can't move further
        if len(contour) < 4:
            continue            # Skip this contour, but maybe some later in the list will be big enough

        # If we continue, then this contour is at least big enough to form rectangle
        # Now we want to simplify it
        reduced_contour : list[tuple[int, int]] = []
        reduced_contour.append(contour[0])                  # Add starting point from this contour

        for i in range(1, len(contour) - 1):
            prev_contour = contour[i - 1]
            curr_contour = contour[i]
            next_contour = contour[i + 1]

            # Find direction (x and y point) before and after
            dir_1_x, dir_1_y = curr_contour[0] - prev_contour[0], curr_contour[1] - prev_contour[1]
            dir_2_x, dir_2_y = next_contour[0] - curr_contour[0], next_contour[1] - curr_contour[1]

            # If there is change in direction - that's a corner, keep it
            if (dir_1_x, dir_1_y) != (dir_2_x, dir_2_y):
                reduced_contour.append(curr_contour)

        # Add the final point from this contour
        reduced_contour.append(contour[-1])

        simplified_contours.append(reduced_contour)

    return simplified_contours

def simplify_contours_with_tolerance(list_of_contours: list[list[tuple[int, int]]], angle_tolerance: int) -> list[list[tuple[int, int]]] | None:
    """
    This is exact same implementation as `simplify_contours`, but doesn't perform strict direction comparison with
    (d1x, d1y) != (d2x, d2y), rather, it takes a specific angle tolerance
    """

    print(f"Simplifying the contours, with {angle_tolerance} degrees tolerance.")
    simplified_contours = []

    for contour in list_of_contours:
        # We need at least 4 points to make a rectangle contour, if not present, we can't move further
        if len(contour) < 4:
            continue  # Skip this contour, but maybe some later in the list will be big enough

        contour = smooth_contour(contour, kernel_size=5)

        # If we continue, then this contour is at least big enough to form rectangle
        # Now we want to simplify it
        reduced_contour: list[tuple[int, int]] = []
        reduced_contour.append(contour[0])  # Add starting point from this contour

        for i in range(1, len(contour) - 1):
            prev_contour = contour[i - 1]
            curr_contour = contour[i]
            next_contour = contour[i + 1]

            # Find direction (x and y point) before and after
            dir_1_x, dir_1_y = curr_contour[0] - prev_contour[0], curr_contour[1] - prev_contour[1]
            dir_2_x, dir_2_y = next_contour[0] - curr_contour[0], next_contour[1] - curr_contour[1]

            # Find the angle of each direction - in RADIANS
            direction_1_angle_rad = math.atan2(dir_1_y, dir_1_x)
            direction_2_angle_rad = math.atan2(dir_2_y, dir_2_x)

            # If there is change in direction, but with {angle} degrees tolerance, keep it
            if abs(direction_1_angle_rad - direction_2_angle_rad) > math.radians(angle_tolerance):
                reduced_contour.append(curr_contour)

        # Add the final point from this contour
        reduced_contour.append(contour[-1])

        simplified_contours.append(reduced_contour)

    return simplified_contours


def smooth_contour(contour, kernel_size=5):
    """Apply simple moving average smoothing to contour points."""
    if len(contour) < kernel_size:
        return contour

    contour = np.array(contour, dtype=np.float32)
    kernel = np.ones(kernel_size) / kernel_size
    x_smooth = np.convolve(contour[:, 0], kernel, mode='same')
    y_smooth = np.convolve(contour[:, 1], kernel, mode='same')
    return np.stack((x_smooth, y_smooth), axis=1).astype(int).tolist()