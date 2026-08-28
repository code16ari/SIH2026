from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.upload import router as upload_router
from routes.process import router as process_router
from routes.result import router as result_router
from routes.evaluation import router as evaluation_router


app = FastAPI(
    title="SIH Satellite Super Resolution API",
    description="Backend for Deep Learning Based Super Resolution Mapping",
    version="1.0.0"
)

# Allow our HTML + JavaScript frontend to communicate
# with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    upload_router, prefix="/api"
    )

app.include_router(
    process_router,
    prefix="/api"
)

app.include_router(
    result_router,
    prefix="/api"
)

app.include_router(
    evaluation_router,
    prefix="/api"
)

@app.get("/")
def root():
    return {
        "message": "SIH Super Resolution Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


from fastapi.responses import FileResponse
import os


@app.get("/api/download/{image_id}")
async def download_result(image_id: str):

    file_path = f"outputs/{image_id}_sr.png"

    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "Result file not found"
        }

    return FileResponse(
        path=file_path,
        media_type="image/png",
        filename=f"{image_id}_super_resolved.png"
    )