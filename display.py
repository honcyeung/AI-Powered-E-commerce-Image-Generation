import matplotlib.pyplot as plt
from PIL import Image

IMAGE_PATH = "./images/"
EDITED_IMAGE_PATH = "./edited_images/"

def display_images_side_by_side(unique_id):

    image1_path = f"{IMAGE_PATH}/{unique_id}.jpg"
    image2_path = f"{EDITED_IMAGE_PATH}/{unique_id}_edited.jpg"
    try:
        img1 = Image.open(image1_path)
        img2 = Image.open(image2_path)

        fig, axes = plt.subplots(1, 2, figsize = (10, 5))

        axes[0].imshow(img1)
        axes[0].set_title('Original')
        axes[0].axis('off')  

        axes[1].imshow(img2)
        axes[1].set_title('Enhanced')
        axes[1].axis('off')  

        plt.tight_layout(pad = 1.5)
        plt.show()

    except FileNotFoundError as e:
        print(f"Error: One of the files was not found. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# display_images_side_by_side("0924eef9e3367c86a43073853040f2cb4a228f33a25932e7d13a4e1c8d45f941")
