from PIL import Image
import os


OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def process_image(input_path: str, output_path: str):
    """
    Temporary Super Resolution processor.

    This currently performs 2x image upscaling.
    Later this function will be replaced by
    the actual Deep Learning Super Resolution model.
    """

    image = Image.open(input_path)

    # 2x upscaling
    new_width = image.width * 2
    new_height = image.height * 2

    enhanced_image = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    enhanced_image.save(output_path)

    return {
        "original_width": image.width,
        "original_height": image.height,
        "output_width": enhanced_image.width,
        "output_height": enhanced_image.height
    }