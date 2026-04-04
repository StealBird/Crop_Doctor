import numpy as np
import json
import os
from PIL import Image
import io

# Smart import — works on both local PC and Render server
try:
    from ai_edge_litert.interpreter import Interpreter as tflite_Interpreter
    def get_interpreter(model_path):
        interp = tflite_Interpreter(model_path=model_path)
        return interp
except ImportError:
    try:
        import tflite_runtime.interpreter as tflite
        def get_interpreter(model_path):
            return tflite.Interpreter(model_path=model_path)
    except ImportError:
        import tensorflow as tf
        def get_interpreter(model_path):
            return tf.lite.Interpreter(model_path=model_path)


# Load models once on startup
BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE, "model", "model.tflite")
CLASSES_PATH = os.path.join(BASE, "model", "class_names.json")

# Disease Model
interpreter = get_interpreter(MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Plant Gate Model (MobileNetV1/V2 TFLite)
GATE_MODEL_PATH = os.path.join(BASE, "model", "mobilenet_v1.tflite")
gate_interpreter = get_interpreter(GATE_MODEL_PATH)
gate_interpreter.allocate_tensors()
gate_input_details = gate_interpreter.get_input_details()
gate_output_details = gate_interpreter.get_output_details()

with open(CLASSES_PATH) as f:
    CLASS_NAMES = json.load(f)

# Hardcoded ImageNet blacklist to block obvious non-plants
# - People (0-99)
# - Mammals (151-270)
# - Birds (271-350)
# - Vehicles (400-530)
# - Furniture (560-700)
# - Electronics/Computers/Phones (~700-880)
# - Cooked food/dishes (924-969)
def is_blacklisted(idx):
    if 0 <= idx <= 99: return True
    if 151 <= idx <= 270: return True
    if 271 <= idx <= 350: return True
    if 400 <= idx <= 530: return True
    if 560 <= idx <= 700: return True
    if 700 <= idx <= 880: return True 
    if 924 <= idx <= 935: return True
    return False

print(f"✅ Models loaded — {len(CLASS_NAMES)} disease classes ready. Blacklist gate active.")

# ── Solutions database ─────────────────────────────────────────
SOLUTIONS = {
    "Tomato___Early_blight": {
        "cause": "Fungus — Alternaria solani",
        "symptoms": "Dark brown spots with yellow rings on lower leaves, spreads upward",
        "severity": "Moderate",
        "organic_cure": "Spray neem oil (5ml/L water) every 7 days. Remove infected leaves immediately.",
        "chemical_cure": "Mancozeb 75% WP @ 2g/L or Chlorothalonil @ 2ml/L every 10 days",
        "prevention": "Crop rotation every 2-3 years, avoid overhead watering, remove plant debris",
        "recovery_time": "2-3 weeks with consistent treatment"
    },
    "Tomato___Late_blight": {
        "cause": "Oomycete — Phytophthora infestans",
        "symptoms": "Water-soaked dark lesions on leaves and stems, white fuzzy mold underneath",
        "severity": "Severe",
        "organic_cure": "Copper-based spray (Bordeaux mixture 1%) every 5-7 days. Remove infected plants.",
        "chemical_cure": "Metalaxyl + Mancozeb (Ridomil Gold) @ 2.5g/L, spray every 7 days",
        "prevention": "Plant resistant varieties, ensure good air circulation, avoid wet foliage at night",
        "recovery_time": "3-4 weeks — act immediately, spreads very rapidly"
    },
    "Tomato___Bacterial_spot": {
        "cause": "Bacteria — Xanthomonas campestris",
        "symptoms": "Small water-soaked spots on leaves, fruit with raised scab-like spots",
        "severity": "Moderate",
        "organic_cure": "Copper hydroxide spray, remove infected plant parts, avoid overhead irrigation",
        "chemical_cure": "Copper oxychloride @ 3g/L every 7-10 days",
        "prevention": "Use disease-free certified seeds, crop rotation, avoid working in wet fields",
        "recovery_time": "3-4 weeks"
    },
    "Tomato___Leaf_Miner": {
        "cause": "Insect pest — Liriomyza trifolii larvae",
        "symptoms": "Irregular white/yellow winding tunnels (mines) on leaf surface",
        "severity": "Mild to Moderate",
        "organic_cure": "Neem oil spray, yellow sticky traps, remove heavily mined leaves",
        "chemical_cure": "Abamectin @ 0.5ml/L or Spinosad @ 0.3ml/L",
        "prevention": "Use reflective mulch, monitor regularly, introduce natural predators",
        "recovery_time": "2-3 weeks"
    },
    "Tomato___Septoria_leaf_spot": {
        "cause": "Fungus — Septoria lycopersici",
        "symptoms": "Small circular spots with dark border and light gray center, lower leaves first",
        "severity": "Moderate",
        "organic_cure": "Remove infected leaves, copper-based fungicide, improve air circulation",
        "chemical_cure": "Chlorothalonil or Mancozeb @ 2g/L every 7-10 days",
        "prevention": "Avoid wetting leaves, mulch around base, crop rotation",
        "recovery_time": "2-3 weeks"
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "cause": "Pest — Tetranychus urticae (tiny spider mites)",
        "symptoms": "Yellow stippling on leaves, fine webbing under leaves, leaves turn bronze",
        "severity": "Moderate",
        "organic_cure": "Spray strong water jet to dislodge mites, neem oil spray, introduce predatory mites",
        "chemical_cure": "Abamectin @ 0.5ml/L or Spiromesifen @ 1ml/L",
        "prevention": "Maintain humidity, avoid dusty conditions, avoid broad-spectrum pesticides",
        "recovery_time": "2-3 weeks"
    },
    "Tomato___Target_Spot": {
        "cause": "Fungus — Corynespora cassiicola",
        "symptoms": "Circular brown spots with concentric rings resembling a target on leaves",
        "severity": "Moderate",
        "organic_cure": "Remove infected leaves, neem oil spray, improve ventilation",
        "chemical_cure": "Azoxystrobin or Difenoconazole @ 1ml/L",
        "prevention": "Crop rotation, avoid excessive nitrogen, proper plant spacing",
        "recovery_time": "2-3 weeks"
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "cause": "Virus — TYLCV transmitted by whiteflies",
        "symptoms": "Yellowing and upward curling of leaves, stunted growth, flower drop",
        "severity": "Severe",
        "organic_cure": "Remove and destroy infected plants immediately, use reflective mulch to repel whiteflies",
        "chemical_cure": "No cure for virus — control whitefly vector with Imidacloprid @ 0.5ml/L",
        "prevention": "Use resistant varieties, install insect-proof nets, monitor whitefly populations",
        "recovery_time": "No recovery — remove infected plants to prevent spread"
    },
    "Tomato___Tomato_mosaic_virus": {
        "cause": "Virus — ToMV, spread by contact and tools",
        "symptoms": "Mosaic pattern of light and dark green on leaves, distorted leaves, reduced yield",
        "severity": "Moderate to Severe",
        "organic_cure": "Remove infected plants, disinfect tools with bleach solution",
        "chemical_cure": "No chemical cure — focus on prevention and removal",
        "prevention": "Use virus-free certified seeds, wash hands before handling plants, control aphids",
        "recovery_time": "No recovery — remove infected plants"
    },
    "Tomato___healthy": {
        "cause": "None",
        "symptoms": "No disease detected — plant looks healthy",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Continue regular monitoring, balanced fertilization, proper watering",
        "recovery_time": "Not applicable"
    },
    "Potato___Early_blight": {
        "cause": "Fungus — Alternaria solani",
        "symptoms": "Brown spots with concentric rings on older/lower leaves first",
        "severity": "Moderate",
        "organic_cure": "Neem oil spray, remove infected leaves, improve drainage",
        "chemical_cure": "Mancozeb 75% WP @ 2g/L or Iprodione @ 2ml/L every 10 days",
        "prevention": "Use certified disease-free seed tubers, crop rotation every 3 years",
        "recovery_time": "2-3 weeks"
    },
    "Potato___Late_blight": {
        "cause": "Oomycete — Phytophthora infestans",
        "symptoms": "Dark water-soaked lesions on leaves, white sporulation under leaves in humid weather",
        "severity": "Severe",
        "organic_cure": "Bordeaux mixture spray, destroy infected plants immediately, do not compost",
        "chemical_cure": "Cymoxanil + Mancozeb @ 3g/L every 7 days, Metalaxyl for severe cases",
        "prevention": "Resistant varieties, avoid excessive irrigation, ensure good field drainage",
        "recovery_time": "4-5 weeks — extremely destructive, act within 24 hours of detection"
    },
    "Potato___healthy": {
        "cause": "None",
        "symptoms": "No disease detected — plant looks healthy",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Regular monitoring, balanced NPK fertilization",
        "recovery_time": "Not applicable"
    },
    "Corn_(maize)___Common_rust_": {
        "cause": "Fungus — Puccinia sorghi",
        "symptoms": "Brick-red to brown pustules (raised bumps) scattered on both leaf surfaces",
        "severity": "Moderate",
        "organic_cure": "Sulfur-based fungicide spray, remove heavily infected leaves",
        "chemical_cure": "Propiconazole @ 1ml/L or Tebuconazole @ 1ml/L, spray at first sign",
        "prevention": "Plant resistant hybrids, early planting to avoid peak humidity season",
        "recovery_time": "2-3 weeks"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "cause": "Fungus — Exserohilum turcicum",
        "symptoms": "Long gray-green to tan cigar-shaped lesions on leaves, starts on lower leaves",
        "severity": "Moderate to Severe",
        "organic_cure": "Remove infected leaves, improve air circulation, avoid dense planting",
        "chemical_cure": "Azoxystrobin or Propiconazole @ 1ml/L at early tasseling stage",
        "prevention": "Resistant varieties, crop rotation, balanced nitrogen fertilization",
        "recovery_time": "3-4 weeks"
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "cause": "Fungus — Cercospora zeae-maydis",
        "symptoms": "Rectangular gray to tan lesions with distinct borders, parallel to leaf veins",
        "severity": "Moderate",
        "organic_cure": "Improve field drainage, remove crop debris, avoid dense canopy",
        "chemical_cure": "Strobilurin fungicides (Azoxystrobin) @ 1ml/L",
        "prevention": "Resistant hybrids, crop rotation, reduce surface residue",
        "recovery_time": "3-4 weeks"
    },
    "Corn_(maize)___healthy": {
        "cause": "None",
        "symptoms": "No disease detected — plant looks healthy",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Balanced fertilization, proper spacing, regular monitoring",
        "recovery_time": "Not applicable"
    },
    "Rice___Brown_spot": {
        "cause": "Fungus — Cochliobolus miyabeanus",
        "symptoms": "Oval to circular brown spots with yellow halo on leaves and grain",
        "severity": "Moderate",
        "organic_cure": "Seed treatment with hot water (52°C for 10 min), balanced potassium fertilization",
        "chemical_cure": "Tricyclazole or Propiconazole @ 1ml/L at tillering and heading stages",
        "prevention": "Use healthy certified seeds, balanced nutrition especially potassium and silicon",
        "recovery_time": "2-3 weeks"
    },
    "Rice___Leaf_blast": {
        "cause": "Fungus — Magnaporthe oryzae",
        "symptoms": "Diamond-shaped gray lesions with brown borders on leaves, neck blast on panicle",
        "severity": "Severe",
        "organic_cure": "Silicon fertilization strengthens cell walls, avoid excess nitrogen",
        "chemical_cure": "Tricyclazole 75% WP @ 0.6g/L or Isoprothiolane @ 1.5ml/L",
        "prevention": "Resistant varieties, balanced nitrogen, avoid dense planting, drain fields periodically",
        "recovery_time": "3-4 weeks — neck blast can cause 100% yield loss if untreated"
    },
    "Rice___Bacterial_leaf_blight": {
        "cause": "Bacteria — Xanthomonas oryzae pv. oryzae",
        "symptoms": "Water-soaked lesions on leaf margins turning yellow then white, wilting",
        "severity": "Severe",
        "organic_cure": "Drain flooded fields, avoid excess nitrogen, remove infected tillers",
        "chemical_cure": "Copper oxychloride @ 3g/L, Streptomycin + Tetracycline combination",
        "prevention": "Resistant varieties, balanced fertilization, avoid flood water movement between fields",
        "recovery_time": "4-6 weeks"
    },
    "Rice___healthy": {
        "cause": "None",
        "symptoms": "No disease detected — plant looks healthy",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Balanced NPK, proper water management, regular field monitoring",
        "recovery_time": "Not applicable"
    },
    "Wheat___Yellow_Rust": {
        "cause": "Fungus — Puccinia striiformis",
        "symptoms": "Yellow-orange pustules in stripes along leaf veins, yellow powdery spores",
        "severity": "Severe",
        "organic_cure": "Remove infected plants, improve air circulation, avoid dense sowing",
        "chemical_cure": "Propiconazole @ 1ml/L or Tebuconazole @ 1ml/L at first sign of disease",
        "prevention": "Resistant varieties, balanced nitrogen, early sowing to avoid cool humid periods",
        "recovery_time": "3-4 weeks"
    },
    "Wheat___Brown_rust": {
        "cause": "Fungus — Puccinia triticina",
        "symptoms": "Round to oval orange-brown pustules on upper leaf surface",
        "severity": "Moderate",
        "organic_cure": "Sulfur dust application, remove infected crop debris",
        "chemical_cure": "Propiconazole 25% EC @ 1ml/L or Mancozeb @ 2.5g/L",
        "prevention": "Resistant varieties, timely sowing, balanced fertilization",
        "recovery_time": "2-3 weeks"
    },
    "Pepper,_bell___Bacterial_spot": {
        "cause": "Bacteria — Xanthomonas campestris pv. vesicatoria",
        "symptoms": "Water-soaked spots on leaves turning brown with yellow halo, fruit lesions",
        "severity": "Moderate",
        "organic_cure": "Copper-based spray, remove infected leaves, avoid overhead irrigation",
        "chemical_cure": "Copper hydroxide @ 2g/L every 7-10 days",
        "prevention": "Use certified seeds, crop rotation, avoid working in wet conditions",
        "recovery_time": "3-4 weeks"
    },
    "Pepper,_bell___healthy": {
        "cause": "None",
        "symptoms": "No disease detected — plant looks healthy",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Regular monitoring, proper irrigation, balanced nutrition",
        "recovery_time": "Not applicable"
    },
    "Apple___Apple_scab": {
        "cause": "Fungus — Venturia inaequalis",
        "symptoms": "Olive-green to black scab-like lesions on leaves and fruit surface",
        "severity": "Moderate",
        "organic_cure": "Sulfur spray every 7-10 days, remove fallen infected leaves",
        "chemical_cure": "Captan or Myclobutanil @ 2g/L from green tip stage",
        "prevention": "Resistant varieties, remove fallen leaves, prune for air circulation",
        "recovery_time": "3-4 weeks"
    },
    "Apple___Black_rot": {
        "cause": "Fungus — Botryosphaeria obtusa",
        "symptoms": "Purple spots on leaves, fruit with concentric ring rot turning black",
        "severity": "Severe",
        "organic_cure": "Remove mummified fruit, prune dead wood, copper spray",
        "chemical_cure": "Captan or Thiophanate-methyl @ 2g/L",
        "prevention": "Remove dead wood and mummified fruit, maintain tree vigor",
        "recovery_time": "4-6 weeks"
    },
    "Apple___Cedar_apple_rust": {
        "cause": "Fungus — Gymnosporangium juniperi-virginianae",
        "symptoms": "Bright orange-yellow spots on upper leaf surface, tube-like structures below",
        "severity": "Moderate",
        "organic_cure": "Remove nearby juniper/cedar trees if possible, sulfur spray",
        "chemical_cure": "Myclobutanil or Propiconazole @ 1ml/L from pink bud stage",
        "prevention": "Resistant apple varieties, remove alternate hosts (junipers) nearby",
        "recovery_time": "2-3 weeks per season"
    },
    "Apple___healthy": {
        "cause": "None",
        "symptoms": "No disease detected — plant looks healthy",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Regular pruning, balanced fertilization, pest monitoring",
        "recovery_time": "Not applicable"
    },
    "Grape___Black_rot": {
        "cause": "Fungus — Guignardia bidwellii",
        "symptoms": "Tan spots with dark borders on leaves, fruit shrivels to black mummies",
        "severity": "Severe",
        "organic_cure": "Remove mummified fruit and infected canes, copper spray",
        "chemical_cure": "Myclobutanil or Captan @ 2g/L from early shoot growth",
        "prevention": "Remove all mummified fruit, proper canopy management for air flow",
        "recovery_time": "4-6 weeks — can cause 100% fruit loss if untreated"
    },
    "Grape___Esca_(Black_Measles)": {
        "cause": "Fungal complex — Phaeomoniella, Phaeoacremonium, Fomitiporia",
        "symptoms": "Tiger-stripe pattern on leaves, dark streaking in wood, berry shriveling",
        "severity": "Severe",
        "organic_cure": "No effective organic cure — remove and destroy infected vines",
        "chemical_cure": "No effective chemical cure — prevention is critical",
        "prevention": "Protect pruning wounds with fungicide paste, use clean pruning tools",
        "recovery_time": "No recovery — infected vines decline over years"
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "cause": "Fungus — Pseudocercospora vitis",
        "symptoms": "Angular dark brown spots on older leaves, premature defoliation",
        "severity": "Moderate",
        "organic_cure": "Remove infected leaves, copper spray, improve air circulation",
        "chemical_cure": "Mancozeb or Captan @ 2g/L every 10-14 days",
        "prevention": "Proper canopy management, avoid overhead irrigation",
        "recovery_time": "3-4 weeks"
    },
    "Grape___healthy": {
        "cause": "None",
        "symptoms": "No disease detected — plant looks healthy",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Regular pruning, balanced nutrition, proper trellis management",
        "recovery_time": "Not applicable"
    },
}

def get_solution(class_name):
    # Try exact match
    if class_name in SOLUTIONS:
        return SOLUTIONS[class_name]
    # Try normalised match
    normalised = class_name.replace(" ", "_").replace("-", "_")
    for key in SOLUTIONS:
        if key.lower() == normalised.lower():
            return SOLUTIONS[key]
    # Partial match
    for key in SOLUTIONS:
        if key.lower() in class_name.lower() or class_name.lower() in key.lower():
            return SOLUTIONS[key]
    # Default fallback
    is_healthy = "healthy" in class_name.lower()
    return {
        "cause": "Not required" if is_healthy else "Consult local agricultural extension officer",
        "symptoms": "Plant appears healthy" if is_healthy else "Disease detected — expert consultation recommended",
        "severity": "None" if is_healthy else "Unknown",
        "organic_cure": "Not required" if is_healthy else "Consult your local KVK office",
        "chemical_cure": "Not required" if is_healthy else "Consult your local KVK office",
        "prevention": "Continue good agricultural practices",
        "recovery_time": "Not applicable" if is_healthy else "Consult local expert"
    }

def diagnose_crop(image_bytes: bytes, media_type: str = "image/jpeg") -> dict:
    try:
        # Preprocess base image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((224, 224))
        
        # --- 1) PLANT GATE (MobileNet ImageNet) ---
        # Normalize to [-1, 1] using numpy only for the gate
        gate_array = (np.array(image, dtype=np.float32) / 127.5) - 1.0
        gate_array = np.expand_dims(gate_array, axis=0)

        # However, the user-provided mobilenet_v1_1.0_224_quant.tflite requires uint8. 
        # But per the exact user spec: "normalize to [-1, 1] using numpy only" - we will abide by it. 
        # TFLite Runtime will throw an error if the model specifically demands uint8 and we give float32.
        # To be completely robust and follow their instruction safely, we cast to uint8 if the model expects it,
        # otherwise we use their float32. By default MobileNetV2 uses float32:
        if gate_input_details[0]['dtype'] == np.uint8:
            gate_array = np.array(image, dtype=np.uint8)
            gate_array = np.expand_dims(gate_array, axis=0)
        
        gate_interpreter.set_tensor(gate_input_details[0]['index'], gate_array)
        gate_interpreter.invoke()
        gate_preds = gate_interpreter.get_tensor(gate_output_details[0]['index'])[0]

        gate_top5 = np.argsort(gate_preds)[-5:][::-1]
        
        # Check against blacklist
        all_blacklisted = True
        for idx in gate_top5:
            if not is_blacklisted(idx):
                all_blacklisted = False
                break

        if all_blacklisted:
            return {"error": "not_a_crop"}

        # --- 2) DISEASE PREDICTION ---
        # Disease model expects [0, 1] normalization
        img_array = np.array(image, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Run TFLite inference
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])[0]

        # Get top result
        top_idx = int(np.argmax(predictions))
        confidence = float(predictions[top_idx])
        class_name = CLASS_NAMES[top_idx]

        # Get top 3 predictions
        top3_idx = np.argsort(predictions)[-3:][::-1]
        top3 = [
            {
                "disease": CLASS_NAMES[i].replace("___", " — ").replace("_", " "),
                "confidence": f"{predictions[i]:.1%}"
            }
            for i in top3_idx
        ]

        is_healthy = "healthy" in class_name.lower()
        solution = get_solution(class_name)

        # Clean up display names — use lookup first, fall back to string cleaning
        CROP_CLEAN_NAMES = {
            "Corn (maize)": "Corn",
            "Pepper, bell": "Bell Pepper",
        }
        parts = class_name.replace("___", "|").split("|")
        crop_raw = parts[0].replace("_", " ").strip()
        crop_name = CROP_CLEAN_NAMES.get(crop_raw, crop_raw)
        disease_name = "Healthy" if is_healthy else parts[1].replace("_", " ").strip() if len(parts) > 1 else class_name

        return {
            "crop": crop_name,
            "disease": disease_name,
            "is_healthy": is_healthy,
            "confidence": f"{confidence:.1%}",
            "confidence_score": round(confidence, 4),
            "severity": solution["severity"],
            "cause": solution["cause"],
            "symptoms": solution["symptoms"],
            "organic_cure": solution["organic_cure"],
            "chemical_cure": solution["chemical_cure"],
            "prevention": solution["prevention"],
            "recovery_time": solution["recovery_time"],
            "top_predictions": top3
        }

    except Exception as e:
        return {"error": f"Could not process image: {str(e)}"}