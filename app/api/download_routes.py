from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.services.job_service import job_service

router = APIRouter(
    prefix="/download",
    tags=["Download"]
)


@router.get("/{job_id}")
async def download_zip(job_id: str):

    if not job_service.job_exists(job_id):
        raise HTTPException(
            status_code=404,
            detail="Invalid Job ID"
        )

    paths = job_service.get_job_paths(job_id)

    zip_path = Path(paths["zip_path"])

    if not zip_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Processed ZIP not found"
        )

    return FileResponse(
        path=zip_path,
        filename="Processed_Images.zip",
        media_type="application/zip"
    )


@router.delete("/{job_id}")
async def delete_job(job_id: str):

    deleted = job_service.delete_job(job_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return {
        "success": True,
        "message": "Job deleted successfully."
    }