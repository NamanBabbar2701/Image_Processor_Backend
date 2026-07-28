from fastapi import APIRouter, HTTPException

from app.services.job_service import job_service

router = APIRouter(
    prefix="/result",
    tags=["Result"]
)


@router.get("/{job_id}")
def get_result(job_id: str):

    result = job_service.get_result(job_id)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Result not ready."
        )

    return result