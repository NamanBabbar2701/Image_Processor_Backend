from fastapi import APIRouter,HTTPException

from app.models.process_request import ProcessRequest
from app.models.process_response import ProcessResponse

from app.services.job_service import JobService
from app.services.excel_processor import ExcelProcessor
from app.services.zip_service import ZipService


router = APIRouter(tags=["Processing"])

job_service = JobService()
excel_processor = ExcelProcessor()
zip_service = ZipService()


@router.post(
    "/process",
    response_model=ProcessResponse
)
async def process_excel(
    request: ProcessRequest
):
    
    # ----------------------------
    # Validate JOB
    # ----------------------------
    
    if not job_service.job_exists(
        request.job_id
    ):
        
        raise HTTPException(
            status_code = 404,
            detail = "Invalid Job ID"
        )
        
    # ----------------------------
    # get Job Paths
    # ----------------------------
    
    paths = job_service.get_job_paths(
        request.job_id
    )
    
    # ----------------------------
    # Process Excel
    # ----------------------------
    
    result = excel_processor.process_excel(
        excel_path=request.filepath,
        output_dir=paths["output_dir"],
        debug_dir=paths["debug_dir"],
        log_dir=paths["log_dir"],
        column_mapping= {
            "student_name_column": request.mapping.student_name_column,
            "student_class_column": request.mapping.student_class_column,
            "image_url_column": request.mapping.image_url_column,
        } 
    )
    
    # ----------------------------
    # Create ZIP
    # ----------------------------
    
    zip_service.create_zip(
        output_dir = paths["output_dir"],
        debug_dir = paths["debug_dir"],
        log_dir = paths["log_dir"],
        zip_path = paths["zip_path"]
    )
    
    return {
        "job_id": request.job_id,
        "processed": result["processed"],
        "failed":result["failed"],
        "total":result["total"],
        "report_path":result["report_path"],
        "zip_path":paths["zip_path"]
    }