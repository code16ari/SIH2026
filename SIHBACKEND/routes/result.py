import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse


router = APIRouter(
    prefix="/result",
    tags=["Results"]
)


@router.get("/{image_id}")
def get_result(image_id: str):

    output_filename = f"{image_id}_sr.png"
    output_path = os.path.join(
        "outputs",
        output_filename
    )

    # Check if processed image exists
    if not os.path.exists(output_path):
        raise HTTPException(
            status_code=404,
            detail="Processed image not found"
        )

    return FileResponse(
        output_path,
        media_type="image/png",
        filename=output_filename
    )