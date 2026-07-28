from fastapi import APIRouter,HTTPException,BackgroundTasks

from app.models.process_request import ProcessRequest
from app.models.process_response import ProcessResponse

from app.services.job_service import job_service
from app.services.excel_processor import ExcelProcessor
from app.services.zip_service import ZipService


router = APIRouter(tags=["Processing"])

excel_processor = ExcelProcessor()
zip_service = ZipService()

def process_job(
    request:ProcessRequest,
    paths:dict
):
    print("1. Background task started")
    
    try:
        print("2. Started Excel Processing")
        
        result = excel_processor.process_excel(
            excel_path=request.filepath,
            
            output_dir=paths["output_dir"],
            
            debug_dir=paths["debug_dir"],
            
            log_dir=paths["log_dir"],
            
            column_mapping={
                "student_name_column": request.mapping.student_name_column,
                "student_class_column": request.mapping.student_class_column,
                "image_url_column" : request.mapping.image_url_column,
            },
            
            job_id=request.job_id,
            
            progress_callback=job_service.update_progress
            
        )
        
        print("3. Excel processing finished")
        
        zip_service.create_zip(
            output_dir=paths["output_dir"],
            
            debug_dir=paths["debug_dir"],
            
            log_dir=paths["log_dir"],
            
            zip_path=paths["zip_path"],
            
        )
        
        print("4. ZIP created")
        
        job_service.save_result(
            request.job_id,
            {
                "processed": result["processed"],
                "failed": result["failed"],
                "total": result["total"],
                "report_path": result["report_path"],
                "zip_path": paths["zip_path"]
            }
        )
        
        print("5. Result Saved")
        
        job_service.complete_job(request.job_id)
        
        print("6. Job Created")
        
    except Exception as e:
        print("BACKGROUND ERROR:", e)
        
        import traceback
        traceback.print_exc()
    
@router.post(
    "/process",
    response_model=ProcessResponse
)
async def process_excel(
    request: ProcessRequest,
    background_tasks: BackgroundTasks
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
    
    background_tasks.add_task(
        process_job,
        
        request,
        
        paths
    )
    
    return{
        
        "job_id": request.job_id,

        "processed": 0,

        "failed": 0,

        "total": 0,

        "report_path": "",

        "zip_path": paths["zip_path"]

    }
    
    