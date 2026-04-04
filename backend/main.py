from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from predict import diagnose_crop
import httpx
import os
import json
import io
from PIL import Image
from predict import diagnose_crop

app = FastAPI(title="Crop Doctor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

TRANSLATE_FIELDS = ["cause", "symptoms", "organic_cure", "chemical_cure", "prevention", "recovery_time"]

# The plant validity gate has been moved to predict.py natively

# Static crop name translations — prevents phonetic guessing by Groq
CROP_NATIVE_NAMES = {
    "hindi": {
        "Tomato":      "टमाटर",
        "Potato":      "आलू",
        "Corn":        "मक्का",
        "Rice":        "धान",
        "Wheat":       "गेहूँ",
        "Apple":       "सेब",
        "Grape":       "अंगूर",
        "Bell Pepper": "शिमला मिर्च",
        "Strawberry":  "स्ट्रॉबेरी",
        "Peach":       "आड़ू",
        "Cherry":      "चेरी",
        "Soybean":     "सोयाबीन",
        "Blueberry":   "ब्लूबेरी",
        "Orange":      "संतरा",
    },
    "marathi": {
        "Tomato":      "टोमॅटो",
        "Potato":      "बटाटा",
        "Corn":        "मका",
        "Rice":        "भात",
        "Wheat":       "गहू",
        "Apple":       "सफरचंद",
        "Grape":       "द्राक्ष",
        "Bell Pepper": "ढोबळी मिरची",
        "Strawberry":  "स्ट्रॉबेरी",
        "Peach":       "पीच",
        "Cherry":      "चेरी",
        "Soybean":     "सोयाबीन",
        "Blueberry":   "ब्लूबेरी",
        "Orange":      "संतरा",
    },
    "hinglish": {
        "Tomato":      "Tamatar",
        "Potato":      "Aloo",
        "Corn":        "Makka",
        "Rice":        "Chawal",
        "Wheat":       "Gehun",
        "Apple":       "Seb",
        "Grape":       "Angoor",
        "Bell Pepper": "Shimla Mirch",
        "Strawberry":  "Strawberry",
        "Peach":       "Aaru",
        "Cherry":      "Cherry",
        "Soybean":     "Soyabean",
        "Blueberry":   "Blueberry",
        "Orange":      "Santra",
    },
}


def confidence_label(conf_str: str) -> str:
    """Convert '87.3%' to plain words like 'high certainty'."""
    try:
        val = float(conf_str.replace("%", "").strip())
        if val >= 90: return "very high certainty"
        if val >= 75: return "high certainty"
        if val >= 60: return "moderate certainty"
        return "low certainty — consider a second opinion"
    except Exception:
        return "moderate certainty"


# What the AI visually sees for each disease in the leaf image
VISUAL_CUES = {
    "Early Blight":             "dark brown concentric ring spots (target-board pattern) on lower leaves with yellowing around the lesions",
    "Late Blight":              "water-soaked gray-green lesions rapidly turning brown, with white mold visible on leaf undersides",
    "Leaf Mold":                "pale green to yellow spots on upper leaf surface with olive-brown velvety mold patches underneath",
    "Septoria Leaf Spot":       "small circular spots with dark borders and lighter centers scattered across the leaf surface",
    "Spider Mites":             "fine stippling (tiny pale dots) across the leaf with possible fine webbing on the underside",
    "Target Spot":              "concentric ring lesions similar to a target with dark brown centers and yellow halos",
    "Yellow Leaf Curl Virus":   "upward leaf curling, severe yellowing along leaf margins, and stunted crinkled growth",
    "Mosaic Virus":             "irregular mosaic pattern of light and dark green patches giving a mottled or marbled appearance",
    "Bacterial Spot":           "small water-soaked spots turning dark brown with yellow halos, often on leaf edges",
    "Apple Scab":               "olive-green to brown velvety lesions with feathery margins on the leaf surface",
    "Black Rot":                "circular 'frog-eye' lesions with purple border fading to tan/brown center",
    "Cedar Apple Rust":         "bright orange-yellow spots on the upper leaf surface, sometimes with tube-like structures below",
    "Powdery Mildew":           "white to gray powdery coating on the leaf surface, especially on young growth",
    "Cercospora Leaf Spot":     "rectangular gray lesions running parallel to leaf veins with distinct dark borders",
    "Gray Leaf Spot":           "rectangular gray to tan lesions with distinct borders, parallel to the leaf veins",
    "Common Rust":              "small reddish-brown powdery pustules scattered across both leaf surfaces",
    "Northern Leaf Blight":     "long elliptical grayish-green lesions several centimeters long running along the leaf",
    "Esca":                     "interveinal chlorosis forming a tiger stripe pattern with brown drying at leaf margins",
    "Leaf Blight":              "irregular brown necrotic patches starting at leaf margins spreading inward",
    "Haunglongbing":            "asymmetric blotchy mottling with yellowing that does not follow leaf veins",
    "Leaf Scorch":              "irregular brown scorched patches along leaf edges and tips with sharp margins",
    "Healthy":                  "uniform green coloration with no lesions, spots, or discoloration across the leaf surface",
}

def get_visual_cues(disease: str) -> str:
    for key in VISUAL_CUES:
        if key.lower() in disease.lower() or disease.lower() in key.lower():
            return VISUAL_CUES[key]
    return "characteristic patterns and discoloration consistent with this condition"


async def generate_summary(result: dict, language: str) -> str:
    """Generate a natural, conversational diagnosis explanation via Groq."""
    if not GROQ_API_KEY:
        return ""

    disease    = result.get("disease", "Unknown")
    crop       = result.get("crop", "Unknown")
    conf_str   = result.get("confidence", "?")
    severity   = result.get("severity", "Unknown")
    is_healthy = result.get("is_healthy", False)
    visual     = get_visual_cues(disease)
    conf_words = confidence_label(conf_str)

    lang_instruction = {
        "hindi":    "Write in simple, warm Hindi (Devanagari script). Keep crop and disease names in English.",
        "marathi":  "Write in simple, warm Marathi (Devanagari script). Keep crop and disease names in English.",
        "hinglish": "Write in friendly Hinglish (Roman script). Keep technical names in English.",
        "english":  "Write in clear, warm English.",
    }.get(language, "Write in clear, warm English.")

    if is_healthy:
        prompt = f"""Write 2 warm encouraging sentences as a crop doctor telling a farmer their {crop} is healthy.
Mention what healthy visual signs were detected: {visual}.
Sound like a real caring doctor, not a robot. No bullet points."""
    else:
        prompt = f"""Write exactly 3 sentences as a crop doctor giving a farmer their diagnosis result. Cover:
1. What was detected: {disease} in their {crop} at {conf_str} confidence ({conf_words}).
2. Why the AI thinks this — the specific visual evidence seen in the image: {visual}.
3. Severity is {severity} — give one sentence of honest reassurance or urgency.

Sound like a knowledgeable, warm doctor speaking to a farmer. No bullet points. No headers. Plain flowing text only."""

    system_prompt = f"""You are a helpful Crop Doctor AI assistant.
CRITICAL INSTRUCTION: You MUST write your ENTIRE response in the {language.upper()} language. 
{lang_instruction}
Do NOT output English sentences unless specifically asked to keep technical names in English."""

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
                    "max_tokens": 220,
                    "temperature": 0.7,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                },
            )
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Summary error: {e}")
        return ""


async def translate_result(result: dict, language: str) -> dict:
    """Translate static disease fields into the requested language."""
    if language == "english" or not GROQ_API_KEY:
        return result

    to_translate = {k: result[k] for k in TRANSLATE_FIELDS if result.get(k)}

    lang_instructions = {
        "hindi":    "Translate the values to simple Hindi (Devanagari script). Keep plant/chemical names in English.",
        "marathi":  "Translate the values to simple Marathi (Devanagari script). Keep plant/chemical names in English.",
        "hinglish": "Translate the values to Hinglish (Roman script Hindi mixed with English). Keep technical/chemical names in English.",
    }

    prompt = f"""{lang_instructions.get(language, "Translate to English.")}

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
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            translated = json.loads(raw.strip())
            result.update(translated)
    except Exception as e:
        print(f"Translation error: {e}")

    # Apply static crop name translation (prevents phonetic guesses like 'maz')
    native_crops = CROP_NATIVE_NAMES.get(language, {})
    native_crop = native_crops.get(result.get("crop", ""))
    if native_crop:
        result["crop"] = native_crop

    return result


@app.get("/")
def root():
    return {"message": "Crop Doctor API is running"}


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    language: str = Form(default="english"),
):
    valid_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type and file.content_type not in valid_types:
        return {"error": "Unsupported file format. Please upload a JPEG, PNG, or WEBP image."}

    image_bytes = await file.read()

    # Normalize all uploaded formats (webp, png, etc.) to standard JPEG bytes
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_io = io.BytesIO()
        img.save(img_io, format="JPEG", quality=90)
        jpeg_bytes = img_io.getvalue()
    except Exception as e:
        return {"error": f"Invalid image format or corrupted file: {str(e)}"}

    result = diagnose_crop(jpeg_bytes)

    # Surface model errors directly (e.g. not_a_crop, processing failures)
    if "error" in result:
        return result

    # Generate natural language summary (new field: ai_summary)
    summary = await generate_summary(result, language)
    result["ai_summary"] = summary

    # Translate static fields if needed
    result = await translate_result(result, language)

    return result


@app.post("/chat")
async def chat(body: dict):
    message    = body.get("message", "")
    disease    = body.get("disease", "Unknown")
    crop       = body.get("crop", "Unknown")
    is_healthy = body.get("is_healthy", False)
    language   = body.get("language", "english")

    lang_instruction = {
        "hindi":    "CRITICAL: You MUST reply ONLY in Hindi using Devanagari script (हिंदी). Every word must be in Hindi. Do NOT write English sentences. Technical/chemical names may stay in English.",
        "marathi":  "CRITICAL: You MUST reply ONLY in Marathi using Devanagari script (मराठी). Every word must be in Marathi. Do NOT write English sentences. Technical/chemical names may stay in English.",
        "hinglish": "CRITICAL: You MUST reply in Hinglish — Hindi words in Roman/Latin script mixed with English. Example: 'Aapke tamatar mein yeh bimari hai, neem oil spray karein.' Do NOT use Devanagari script.",
        "english":  "Reply in clear, simple English.",
    }.get(language, "Reply in clear, simple English.")

    system_prompt = f"""You are Crop Doctor, a friendly agricultural AI for Indian farmers.
CRITICAL INSTRUCTION: You MUST reply ONLY in the {language.upper()} language.
{lang_instruction}
Crop: {crop}. Condition: {disease if not is_healthy else 'Healthy — no disease detected'}.
Give practical, concise advice in 2-4 sentences."""

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
            return {"reply": data["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"reply": f"Sorry, something went wrong: {str(e)}"}