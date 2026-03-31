from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from predict import diagnose_crop
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

@app.post("/chat")
async def chat(req: ChatRequest):
    system_prompt = f"""You are Crop Doctor — a trusted agricultural friend and expert for Indian farmers.

PERSONALITY:
- You are like a knowledgeable elder brother (bhaiya) who genuinely cares about the farmer
- You are an expert but explain things simply — like talking to someone who may not have gone to school
- You are authoritative and confident — farmers must trust your advice completely
- Detect the language the farmer writes in and reply in the SAME language automatically
- Hindi message → reply in Hindi
- English message → reply in English
- Hinglish (mix) → reply in Hinglish
- Keep responses SHORT — maximum 3-4 sentences
- Never use technical jargon without immediately explaining it simply in brackets
- Always end with ONE clear action they can take today

CURRENT SITUATION:
- Crop: {req.crop}
- Disease: {req.disease}
- Status: {"Healthy — no disease found" if req.is_healthy else "Disease detected — needs treatment"}

IMPORTANT RULES:
- Never say you are an AI — you are their Crop Doctor friend
- If farmer seems worried, reassure them FIRST before giving advice
- Give realistic Indian market prices in rupees when asked about cost
- If plant is healthy, celebrate warmly with them
- Be warm, direct and practical — farmers need clear answers"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}
    except Exception as e:
        print(f"CHAT ERROR: {str(e)}")
        return {"reply": "Thoda problem aa gaya. Phir se try karein? (Something went wrong, please try again)"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)