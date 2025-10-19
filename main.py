from image_related_ops.load_image import load_image

IMAGE_DIR = "./test_images"
TARGET_IMAGE = "mazda_one.png"

if __name__ == '__main__':

    # Load the image
    img_nparray = load_image(f"{IMAGE_DIR}/{TARGET_IMAGE}")
    print(f"Loaded image's shape: {img_nparray.shape}")

    