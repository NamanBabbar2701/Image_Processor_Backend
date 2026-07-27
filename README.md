# Smart Portrait Cropper - Backend

A FastAPI-based backend for automated portrait photo processing. The system accepts an Excel workbook containing student information and image URLs, downloads each image, detects facial landmarks using MediaPipe Face Mesh, aligns portraits, applies intelligent composition rules, and generates standardized ID-card photographs in batch.

Designed for schools, educational institutions, and organizations that need to process hundreds or thousands of portrait photographs quickly and consistently.

---

## Features

- RESTful FastAPI backend
- Excel workbook upload and validation
- Automatic Excel column mapping
- Batch image downloading from URLs
- Face detection using MediaPipe Face Mesh
- Intelligent face alignment
- Landmark transformation (single FaceMesh detection)
- Intelligent crop planning
- Sub-pixel accurate cropping
- Composition validation and correction
- Image enhancement and sharpening
- Batch processing with processing reports
- ZIP generation for processed images
- Modular service-based architecture

---

## Processing Pipeline

```
Upload Excel
      │
      ▼
Validate Workbook
      │
      ▼
Download Images
      │
      ▼
Detect Face Mesh
      │
      ▼
Analyze Face Geometry
      │
      ▼
Align Portrait
      │
      ▼
Transform Landmarks
      │
      ▼
Plan Intelligent Crop
      │
      ▼
Sub-pixel Crop
      │
      ▼
Validate Composition
      │
      ▼
Image Enhancement
      │
      ▼
Generate Final Portrait
      │
      ▼
ZIP Download
```

---

## Project Structure

```
backend/
│
├── app/
│   ├── api/
│   │   ├── upload_routes.py
│   │   ├── process_routes.py
│   │   ├── download_routes.py
│   │   └── health_routes.py
│   │
│   ├── models/
│   │
│   ├── processor/
│   │   ├── face_mesh.py
│   │   ├── face_analyzer.py
│   │   ├── face_aligner.py
│   │   ├── landmark_transformer.py
│   │   ├── crop_planner.py
│   │   ├── crop_executor.py
│   │   ├── composition_validator.py
│   │   ├── image_enhancer.py
│   │   ├── portrait_processor.py
│   │   └── config.py
│   │
│   ├── services/
│   │   ├── upload_service.py
│   │   ├── job_service.py
│   │   ├── excel_processor.py
│   │   └── zip_service.py
│   │
│   ├── jobs/
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/upload` | Upload Excel workbook |
| POST | `/process` | Process all portraits |
| GET | `/download/{job_id}` | Download processed images |

---

## Installation

Clone the repository

```bash
git clone https://github.com/NamanBabbar2701/Image_Processor_Backend.git
```

Navigate into the project

```bash
cd Image_Processer_Backend
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Backend

Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

API Documentation

```
http://127.0.0.1:8000/docs
```

Interactive ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Workflow

1. Upload an Excel workbook.
2. Select the appropriate columns (Student Name, Class, Image URL).
3. Start batch processing.
4. Images are automatically downloaded and processed.
5. Download the generated ZIP containing processed portraits.

---

## Generated Job Structure

```
jobs/
└── <job_id>/
    ├── upload/
    ├── output/
    ├── debug/
    ├── logs/
    └── output.zip
```

---

## Configuration

Most processing parameters can be customized through:

```
app/processor/config.py
```

Configurable parameters include:

- Output image resolution
- Portrait aspect ratio
- Head width ratio
- Head height ratio
- Eye-line position
- Rotation limits
- Composition validation tolerance
- Image sharpening
- Background padding color

---

## Technologies Used

### Backend

- FastAPI
- Pydantic
- Uvicorn

### Computer Vision

- OpenCV
- MediaPipe Face Mesh
- NumPy

### Data Processing

- Pandas
- Requests

---

## Current Status

### Completed

- Excel Upload API
- Image Processing API
- Download API
- Job Management
- Portrait Processing Pipeline
- Batch Processing
- ZIP Generation
- Processing Reports

### Planned

- Authentication
- Background task processing
- Real-time processing progress
- Docker deployment
- Cloud storage support
- Multiple portrait standards

---

## Frontend

The React frontend for this project is maintained separately.

Repository:

```
https://github.com/NamanBabbar2701/Image_Processor_Frontend.git
```

---

## License

**Copyright © 2026 Naman Babbar**

This project is proprietary software.

The source code is published for reference only. No permission is granted to copy, modify, distribute, sublicense, or use this software without prior written permission from the copyright holder.

---

## Author

**Naman Babbar**