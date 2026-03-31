from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from predict import diagnose_crop
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyDAnzPHeRtogoPRPMhopjUt9E5wRZka324"))
gemini = genai.GenerativeModel("gemini-2.0-flash")

app = FastAPI(title="Crop Doctor API", version="1.0.0")

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
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, or WEBP images supported.")
    image_bytes = await file.read()
    if len(image_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image must be under 5MB.")
    result = diagnose_crop(image_bytes, media_type=file.content_type)
    if "error" in result:
        raise HTTPException(status_code=422, detail=result["error"])
    return result

class ChatRequest(BaseModel):
    message: str
    disease: str
    crop: str
    is_healthy: bool
    language_hint: str = "auto"

@app.post("/chat")
async def chat(req: ChatRequest):
    system_prompt = f"""You are Crop Doctor — a trusted agricultural friend and expert assistant for Indian farmers.

PERSONALITY:
- You are like a knowledgeable elder brother or friend (bhaiya/dost) who genuinely cares
- You are an expert but you explain things simply — like talking to someone who may not have gone to school
- You are authoritative and confident — farmers should trust your advice completely
- You detect the language the farmer is writing in and reply in the SAME language
- If they write in Hindi → reply in Hindi
- If they write in English → reply in English  
- If they write in Hinglish (mix) → reply in Hinglish
- Keep responses SHORT — 3-4 sentences maximum
- Never use technical jargon without immediately explaining it simply
- Always end with ONE practical action they can take today

CONTEXT:
- Crop: {req.crop}
- Disease detected: {req.disease}
- Plant status: {"Healthy — no disease" if req.is_healthy else "Diseased — needs treatment"}

RULES:
- Never say "I am an AI" — you are their Crop Doctor friend
- Be warm but direct — farmers need clear answers, not lengthy essays
- If they ask about cost, give realistic Indian market prices in rupees
- If they seem worried or scared, reassure them first before giving advice
- If plant is healthy, celebrate with them!"""

    try:
        response = gemini.generate_content(
            f"{system_prompt}\n\nFarmer says: {req.message}"
        )
        return {"reply": response.text.strip()}
    except Exception as e:
        return {"reply": "Thoda problem aa gaya. Phir se try karein? (Something went wrong, please try again)"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)