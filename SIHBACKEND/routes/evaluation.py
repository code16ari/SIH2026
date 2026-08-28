import os

import numpy as np
from PIL import Image
from fastapi import APIRouter, HTTPException

from skimage.metrics import (
    peak_signal_noise_ratio,
    structural_similarity
)


router = APIRouter(
    prefix="/evaluate",
    tags=["Evaluation"]
)


@router.get("/{image_id}")
def evaluate_image(image_id: str):

    input_files = [
        filename
        for filename in os.listdir("uploads")
        if filename.startswith(image_id)
    ]

    if not input_files:
        raise HTTPException(
            status_code=404,
            detail="Original image not found"
        )

    input_path = os.path.join(
        "uploads",
        input_files[0]
    )

    output_path = os.path.join(
        "outputs",
        f"{image_id}_sr.png"
    )

    if not os.path.exists(output_path):
        raise HTTPException(
            status_code=404,
            detail="Processed image not found"
        )

    # Open images
    original = Image.open(input_path).convert("RGB")
    sr_image = Image.open(output_path).convert("RGB")

    # Resize original to SR dimensions
    reference = original.resize(
        sr_image.size,
        Image.Resampling.BICUBIC
    )

    # Convert to NumPy arrays
    reference_array = np.array(reference)
    sr_array = np.array(sr_image)

    # RMSE
    mse = np.mean(
        (reference_array.astype(float) -
         sr_array.astype(float)) ** 2
    )

    rmse = np.sqrt(mse)

    # PSNR
    psnr = peak_signal_noise_ratio(
        reference_array,
        sr_array,
        data_range=255
    )

    # SSIM
    ssim = structural_similarity(
        reference_array,
        sr_array,
        channel_axis=2,
        data_range=255
    )

    return {
        "status": "success",
        "image_id": image_id,
        "psnr": round(float(psnr), 4),
        "ssim": round(float(ssim), 4),
        "rmse": round(float(rmse), 4)
    }