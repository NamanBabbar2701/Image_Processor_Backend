from pydantic import BaseModel


class ProcessResponse(BaseModel):

    job_id: str

    processed: int

    failed: int

    total: int

    report_path: str

    zip_path: str