import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("")
async def upload_image(file: UploadFile = File(...)):

    # Allowed file types
    allowed_extensions = [
        ".tif",
        ".tiff",
        ".png",
        ".jpg",
        ".jpeg"
    ]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Use TIFF, PNG, JPG, or JPEG."
        )

    # Generate a unique ID for the uploaded image
    image_id = str(uuid.uuid4())

    filename = f"{image_id}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    # Read uploaded file
    contents = await file.read()

    # Save file
    with open(file_path, "wb") as f:
        f.write(contents)

    return {
        "status": "success",
        "image_id": image_id,
        "filename": filename,
        "message": "Image uploaded successfully"
    }