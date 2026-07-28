from fastapi import APIRouter, HTTPException

from app.services.job_service import job_service

router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)


@router.get("/{job_id}")
def get_progress(job_id: str):

    progress = job_service.get_progress(job_id)

    if progress is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return progress