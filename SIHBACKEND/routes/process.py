import os

from fastapi import APIRouter, HTTPException

from services.processor import process_image


router = APIRouter(
    prefix="/process",
    tags=["Processing"]
)


@router.post("/{image_id}")
def process_uploaded_image(image_id: str):

    # Find uploaded image
    upload_dir = "uploads"

    possible_files = [
        filename
        for filename in os.listdir(upload_dir)
        if filename.startswith(image_id)
    ]

    if not possible_files:
        raise HTTPException(
            status_code=404,
            detail="Uploaded image not found"
        )

    input_filename = possible_files[0]

    input_path = os.path.join(
        upload_dir,
        input_filename
    )

    # Output filename
    output_filename = f"{image_id}_sr.png"

    output_path = os.path.join(
        "outputs",
        output_filename
    )

    # Process image
    result = process_image(
        input_path,
        output_path
    )

    return {
        "status": "success",
        "image_id": image_id,
        "output_file": output_filename,
        "message": "Image processed successfully",
        "details": result
    }