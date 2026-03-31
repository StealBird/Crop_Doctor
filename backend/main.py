from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from predict import diagnose_crop
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()
def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

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
    language: str = "english"

@app.post("/chat")
async def chat(req: ChatRequest):
    lang_instruction = {
        "english": "Always respond in clear simple English only.",
        "hindi": "हमेशा सरल हिंदी में जवाब दो। अंग्रेजी शब्द कम से कम इस्तेमाल करो।",
        "marathi": "नेहमी सोप्या मराठीत उत्तर द्या.",
        "hinglish": "Always respond in Hinglish — mix of Hindi and English naturally like Indians talk.",
    }.get(req.language, "Always respond in clear simple English only.")

    system_prompt = f"""You are Crop Doctor — a trusted agricultural expert for Indian farmers.

LANGUAGE RULE — MOST IMPORTANT:
{lang_instruction}

PERSONALITY:
- Expert and authoritative — farmers must trust your advice completely
- Simple and clear — explain like talking to someone who may not be educated
- Caring but direct — give clear actionable answers
- Keep responses to 3-4 sentences maximum
- End with ONE clear action they can take today

CURRENT SITUATION:
- Crop: {req.crop}
- Disease: {req.disease}
- Status: {"Healthy — no disease found" if req.is_healthy else "Disease detected — needs treatment"}

RULES:
- Never say you are an AI
- Give realistic Indian market prices in rupees when asked about cost
- If plant is healthy, be positive and encouraging
- Reassure worried farmers before giving advice"""

    try:
        response = get_groq_client().chat.completions.create(
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
        return {"reply": "Something went wrong. Please try again."}