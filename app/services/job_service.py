from pathlib import Path
from uuid import uuid4
import shutil


class JobService:

    def __init__(self):

        self.jobs_root = Path("app/jobs")

        self.jobs_root.mkdir(
            parents=True,
            exist_ok=True
        )
        
    def _build_paths(
        self,
        job_dir: Path
    ) -> dict:
        
        return{
            "job_dir": str(job_dir),
            "upload_dir": str(job_dir/ "upload"),
            "output_dir": str(job_dir/ "output"),
            "debug_dir": str(job_dir/ "debug"),
            "log_dir": str(job_dir/  "logs"),
            "zip_path": str(job_dir/  "output.zip"),
        }

    def create_job(self) -> dict:

        job_id = uuid4().hex

        job_dir = self.jobs_root / job_id

        upload_dir = job_dir / "upload"
        output_dir = job_dir / "output"
        debug_dir = job_dir / "debug"
        log_dir = job_dir / "logs"

        upload_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(exist_ok=True)
        debug_dir.mkdir(exist_ok=True)
        log_dir.mkdir(exist_ok=True)

        return {

            "job_id": job_id,
            **self._build_paths(job_dir)

        }
        
    def get_job_paths(
        self,
        job_id: str
    ) -> dict:

        job_dir = self.jobs_root / job_id
        
        if not job_dir.is_dir():
            raise FileNotFoundError(
                f"Job '{job_id}' does not exist"
            )

        return self._build_paths(job_dir)
        
    def job_exists(
        self,
        job_id: str
    ) -> bool:

        return (self.jobs_root / job_id).is_dir()
    
    
    def delete_job(
        self,
        job_id: str
    ) -> bool:
        
        job_dir = self.jobs_root / job_id
        
        if not job_dir.is_dir():
            return False

        shutil.rmtree(job_dir)
        
        return True