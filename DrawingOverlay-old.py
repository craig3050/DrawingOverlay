from PIL import Image

def overlay_images(image1_path, image2_path, transparency=0.5):
    """
    Overlays two images with a given transparency value.

    Parameters:
        image1_path (str): Path to the first image.
        image2_path (str): Path to the second image.
        transparency (float): Transparency level for blending (0 to 1).
                              0 means fully image1, 1 means fully image2.

    Returns:
        None: Displays the overlayed image.
    """
    # Ensure transparency is within the valid range
    if not (0 <= transparency <= 1):
        raise ValueError("Transparency must be between 0 and 1.")

    # Open the images
    image1 = Image.open(image1_path).convert("RGBA")
    image2 = Image.open(image2_path).convert("RGBA")

    # Check if images are the same size
    if image1.size != image2.size:
        raise ValueError("Images must have the same dimensions.")

    # Blend the images
    blended = Image.blend(image1, image2, transparency)

    # Display the blended image
    blended.show()

if __name__ == "__main__":
    # User-defined paths to images
    image1_path = "test3.png"  # Replace with the path to your first layout image
    image2_path = "test4.png"  # Replace with the path to your second layout image

    # User-defined transparency value
    transparency = 0.5  # Adjust this value between 0 and 1 as needed

    # Call the function to overlay images
    overlay_images(image1_path, image2_path, transparency)
