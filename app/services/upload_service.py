import shutil
from pathlib import Path
from uuid import uuid4
import pandas as pd
from fastapi import UploadFile


class UploadService:


    def save_excel(
        self,
        file: UploadFile,
        upload_dir:str
    ) -> dict:
        
        # Extension Check
        
        extension = Path(file.filename).suffix.lower()
        
        allowed = {
            ".xlsx",
            ".xls"
        }
        
        if extension not in  allowed: 
            raise ValueError(
                "Only Excel files are allowed"
            )
            
        #MIME Type Check
        
        content_type = file.content_type
        

        allowed_types = {
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel"
        }
        
        if content_type not in allowed_types:
            raise ValueError(
                "Invalid file type. Only .xlsx and .xls files are allowed"
            )
        
            
        upload_dir = Path(upload_dir)

        upload_dir.mkdir(
            parents=True, 
            exist_ok=True
        )
        
        filename = (
            f"{uuid4().hex}{extension}"
        )
        
        filepath = upload_dir / filename
        
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )
            
            
        try: 
            pd.ExcelFile(filepath)
            
        except Exception:
            filepath.unlink(missing_ok=True)
            
            raise ValueError(
                "Uploaded File is corrupted or is not a valid Excel Workbook"
            )
            

        return {
            "filename": file.filename,
            "filepath": str(filepath)
        }