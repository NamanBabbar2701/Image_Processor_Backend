from pydantic import BaseModel, Field

class ColumnMapping(BaseModel):
    student_name_column: int = Field(..., ge=0)
    student_class_column: int = Field(..., ge=0)
    image_url_column: int = Field(..., ge=0)
    
class ProcessRequest(BaseModel):
    job_id: str
    filepath: str
    mapping: ColumnMapping