from PIL import Image

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

    # Save the image state in current step
    save_current_image_state(gray_img_nparray, TARGET_IMAGE, "1", "grayscale")

    # ------ STEP 1: Grayscale END ------