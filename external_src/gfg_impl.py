"""
Original implementation from source GeeksForGeeks website:
https://www.geeksforgeeks.org/machine-learning/license-plate-recognition-with-opencv-and-tesseract-ocr/
"""

import matplotlib.pyplot as plt
import cv2
import pytesseract

from main import IMAGE_DIR, TARGET_IMAGE


def gfg_implementation():
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