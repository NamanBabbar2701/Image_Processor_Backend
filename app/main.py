from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload_routes import router as upload_router
from app.api.process_routes import router as process_router
from app.api.download_routes import router as download_router
from app.api.progress_routes import router as progress_router
from app.api.result_routes import router as result_router

app = FastAPI(
    title="Smart Portrait Cropper API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://image-processor-alpha.vercel.app",
        ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(process_router)
app.include_router(download_router)
app.include_router(progress_router)
app.include_router(result_router)


@app.get("/")
def home():

    return {
        "message": "Smart Portrait Cropper API is running."
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "Image Processor API",
        "version": "1.0.0"
    }