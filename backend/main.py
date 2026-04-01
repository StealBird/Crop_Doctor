from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from predict import predict_disease
import httpx
import os
import json

app = FastAPI(title="Crop Doctor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Fields from predict result that need translation
TRANSLATE_FIELDS = ["cause", "symptoms", "organic_cure", "chemical_cure", "prevention", "recovery_time"]


async def translate_result(result: dict, language: str) -> dict:
    """Translate the disease result fields into the requested language using Groq."""
    if language == "english" or not GROQ_API_KEY:
        return result

    # Build a compact JSON of only the fields that need translating
    to_translate = {k: result[k] for k in TRANSLATE_FIELDS if result.get(k)}

    lang_instructions = {
        "hindi":    "Translate the values to simple Hindi (Devanagari script). Keep plant/chemical names in English.",
        "marathi":  "Translate the values to simple Marathi (Devanagari script). Keep plant/chemical names in English.",
        "hinglish": "Translate the values to Hinglish (Roman script Hindi mixed with English). Keep technical/chemical names in English.",
    }

    instruction = lang_instructions.get(language, "Translate to English.")

    prompt = f"""{instruction}

Return ONLY a valid JSON object with the same keys. No explanation, no markdown, no backticks.

Input JSON:
{json.dumps(to_translate, ensure_ascii=False)}"""

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "max_tokens": 600,
                    "temperature": 0.1,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            data = response.json()
            raw = data["choices"][0]["message"]["content"].strip()

            # Strip markdown fences if Groq adds them
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            translated = json.loads(raw)
            # Merge translated fields back into result
            result.update(translated)
    except Exception as e:
        # If translation fails for any reason, return original English — never crash
        print(f"Translation error: {e}")

    return result


@app.get("/")
def root():
    return {"message": "Crop Doctor API is running"}


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    language: str = Form(default="english"),   # ← new optional param
):
    image_bytes = await file.read()
    result = predict_disease(image_bytes)

    # Translate the result content if language is not English
    result = await translate_result(result, language)

    return result


@app.post("/chat")
async def chat(body: dict):
    message = body.get("message", "")
    disease = body.get("disease", "Unknown")
    crop = body.get("crop", "Unknown")
    is_healthy = body.get("is_healthy", False)
    language = body.get("language", "english")

    lang_instruction = {
        "hindi":    "You MUST reply only in Hindi (Devanagari script).",
        "marathi":  "You MUST reply only in Marathi (Devanagari script).",
        "hinglish": "You MUST reply only in Hinglish (Roman script Hindi mixed with English).",
        "english":  "Reply in English.",
    }.get(language, "Reply in English.")

    system_prompt = f"""You are Crop Doctor, an expert agricultural assistant for Indian farmers.
{lang_instruction}
Crop: {crop}. Disease: {disease if not is_healthy else 'Healthy — no disease'}.
Give practical, simple advice. Keep responses concise (2-4 sentences)."""

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "max_tokens": 300,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message},
                    ],
                },
            )
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            return {"reply": reply}
    except Exception as e:
        return {"reply": f"Sorry, something went wrong: {str(e)}"}