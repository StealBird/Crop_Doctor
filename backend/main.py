from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from predict import diagnose_crop
import uvicorn

app = FastAPI(
    title="Crop Doctor API",
    description="AI-powered crop disease detection",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Crop Doctor API is running 🌿"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, or WEBP images are supported."
        )

    # Validate file size (max 5MB)
    image_bytes = await file.read()
    if len(image_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Image size must be under 5MB."
        )

    result = diagnose_crop(image_bytes, media_type=file.content_type)

    if "error" in result:
        raise HTTPException(status_code=422, detail=result["error"])

    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)