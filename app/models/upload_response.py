from typing import List
from pydantic import BaseModel

class UploadResponse(BaseModel):
    job_id: str
    filename: str
    filepath: str
    columns : List[str]