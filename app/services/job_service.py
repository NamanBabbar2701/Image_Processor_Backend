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
        
        self.progress={}
        
        self.results={}
        
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
        
        self.progress[job_id] = {
            "status": "created",
            "current": 0,
            "total": 0,
            "student": "",
            "percentage": 0,
            "completed": False
            
        }

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
        
        if job_id in self.progress:
            del self.progress[job_id]
        
        return True
    
    def update_progress(
        self,
        job_id: str,
        current: int,
        total: int,
        student_name: str
    ):
        percentage = (
            int((current / total) * 100)
            if total > 0
            else 0
)

        if job_id not in self.progress:
            return

        self.progress[job_id]["status"] = "processing"

        self.progress[job_id]["current"] = current

        self.progress[job_id]["total"] = total

        self.progress[job_id]["student"] = student_name
        
        self.progress[job_id]["percentage"] = percentage
        
        self.progress[job_id]["completed"] = False
        
    def complete_job(
        self,
        job_id: str
    ):
        
        print("=" * 50)
        print("COMPLETE JOB CALLED")
        print("Job ID:", job_id)
        

        if job_id not in self.progress:
            print("NOT FOUND")
            print(self.progress)
            return

        self.progress[job_id]["status"] = "completed"
        self.progress[job_id]["completed"] = True
        
        print("UPDATED:")
        print(self.progress[job_id])
        print("=" * 50)
        
    def get_progress(
        self,
        job_id: str
    ):

        progress = self.progress.get(job_id)
        print("GET PROGRESS:")
        print(progress)
        
        return progress
    
    def save_result(
        self,
        job_id: str,
        result: dict
    ):

        self.results[job_id] = result
        
    def get_result(
        self,
        job_id: str
    ):
        return self.results.get(job_id)
        
job_service = JobService();