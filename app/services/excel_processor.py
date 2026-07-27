import re
import cv2
import numpy as np
import pandas as pd
import requests
from pathlib import Path



from app.processor.portrait_processor import PortraitProcessor


class ExcelProcessor:

    def __init__(self):

        self.processor = PortraitProcessor()

    def clean_filename(self, 
                       text : str) -> str:

        text = str(text).strip()

        return re.sub(r'[<>:"/\\\\|?*]', "", text)
    
    def get_call(
        self,
        row,
        column_index: int
    ) -> str:
        
        value = row.iloc[column_index]
        
        if pd.isna(value):
            return ""
        
        return str(value).strip()
        
    def add_report(
        self,
        report,
        excel_row,
        student_name,
        student_class,
        status,
        reason=""
    ):
        report.append({
            "Excel Row" : excel_row,
            "Student" : student_name,
            "Class" : student_class,
            "Status": status,
            "Reason" : reason
            
        })
        

    
    def download_image(
        self,
        image_url: str,
        timeout: int
    ):

        response = requests.get(
            image_url,
            timeout=timeout,
            headers={
                "User-Agent": "ImageProcessor/1.0"
            }
        )

        response.raise_for_status()

        image_array = np.asarray(
            bytearray(response.content),
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )
        
        if image is None:
            raise ValueError("Invalid image")
        
        return image
        
    def save_images(
        self,
        final_image,
        debug_image,
        output_path,
        debug_path
    ):

        cv2.imwrite(
            output_path,
            final_image
        )
        
        if debug_image is not None:

            cv2.imwrite(
                debug_path,
                debug_image
            )
        
    def build_paths(
        self,
        student_name,
        student_class,
        output_dir,
        debug_dir
    ):
        
        filename = (
            f"{self.clean_filename(student_class)}_"
            f"{self.clean_filename(student_name)}.jpg"
        )
        
        output_path = Path(output_dir) / filename
        debug_path = Path(debug_dir) / filename
        
        return str(output_path), str(debug_path)
        
        
    def save_report(
        self,
        report,
        log_dir
    ):

        report_df = pd.DataFrame(report)

        report_path = Path(log_dir) / "processing_report.csv"

        report_df.to_csv(
            report_path,
            index=False
        )

        return str(report_path)
    
    def process_row(
        self,
        image_url,
        timeout
    ):
        
        try:
        
            image = self.download_image(
                image_url,
                timeout
            )    
            
            return self.processor.process(image)
            
    
            
        except Exception as e:
            
            return {
                "success" : False,
                "status": "Failed",
                "reason": str(e),
                "final_image": None,
                "debug_image": None
            }
            
    # ------------------------
    # MAIN PROCESSING
    # ------------------------

    def process_excel(
        self,
        excel_path,
        output_dir,
        debug_dir,
        log_dir,
        column_mapping,
        timeout=20,
        progress_callback=None
    ):

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        Path(debug_dir).mkdir(parents=True, exist_ok=True)
        Path(log_dir).mkdir(parents=True, exist_ok=True)

        report = []

        df = pd.read_excel(
            excel_path,
            engine="openpyxl"
        )
        
        # -------------------------
        # Validate Column Mapping
        # -------------------------  
        
        for key, index in column_mapping.items():
            
            if index < 0 or index >= len(df.columns):
                raise ValueError(
                    f"Invalid column index for '{key}'"
                )             

        total = len(df)
        processed = 0
        failed = 0
        
        # ------------------------
        # Process Every Row
        # ------------------------
        
        
        for index, row in df.iterrows():
            excel_row = index + 2
            
            student_name = self.get_call(
                row,
                column_mapping["student_name_column"]
            )
            
            student_class = self.get_call(
                row,
                column_mapping["student_class_column"]
            )
            
            image_url = self.get_call(
                row,
                column_mapping["image_url_column"]
            )
            
            
            # --------------------------
            # Skip empty URL
            # --------------------------
            
            
            if not image_url:
                
                self.add_report(
                    report,
                    excel_row,
                    student_name,
                    student_class,
                    "Skipped",
                    "Empty URL",
                )
                
                failed += 1 
        
                if progress_callback:

                    progress_callback(
                            current=index + 1,
                            total=total
                    )
                
                continue
        
            # --------------------
            # Output Paths
            # --------------------
            
            output_path, debug_path  = self.build_paths(
                student_name,
                student_class,
                output_dir,
                debug_dir
            )
            
            # ----------------------
            # Process One Image
            # ----------------------
            
            result = self.process_row(
                image_url,
                timeout
            )
            
            if result["success"]:
                
                self.save_images(
                    result["final_image"],
                    result["debug_image"],
                    output_path,
                    debug_path
                )
                
                processed += 1
                
            else:
                
                failed += 1
                
            self.add_report(
                report,
                excel_row,
                student_name,
                student_class,
                result["status"],
                result["reason"]
            )
            
            
            # --------------------
            # Progress
            # --------------------
            
            if progress_callback:
                
                progress_callback(
                    current = index +1,
                    total = total
                )

        # --------------------
        # Save Report
        # --------------------
   
        report_path = self.save_report(
            report,
            log_dir
        )
         
        return {
            "processed": processed,
            
            "failed": failed,
            
            "total": total,
            
            "report_path": report_path,
            
            "output_directory" : output_dir,
            
            "debug_directory" : debug_dir
        }