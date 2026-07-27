from fastapi import APIRouter, UploadFile, File

from app.models.upload_response import UploadResponse
from app.services.upload_service import UploadService
from app.services.exel_service import ExcelService
from app.services.job_service import JobService

router = APIRouter()

job_service = JobService()
upload_service = UploadService()
excel_service = ExcelService()


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_excel(
    file: UploadFile = File(...)
):
    job = job_service.create_job()

    upload = upload_service.save_excel(
        file = file,
        upload_dir=job["upload_dir"])
    
    columns = excel_service.read_columns(
        upload["filepath"]
    )

    return {
        "job_id": job["job_id"],
        "filename": upload["filename"],
        "filepath": upload["filepath"],
        "columns": columns
    }