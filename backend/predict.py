import numpy as np
import json
import os
from PIL import Image
import io

# Smart import — works on both local PC and Render server
try:
    from ai_edge_litert.interpreter import Interpreter as tflite_Interpreter
    def get_interpreter(model_path):
        return tflite_Interpreter(model_path=model_path)
except ImportError:
    try:
        import tflite_runtime.interpreter as tflite
        def get_interpreter(model_path):
            return tflite.Interpreter(model_path=model_path)
    except ImportError:
        import tensorflow as tf
        def get_interpreter(model_path):
            return tf.lite.Interpreter(model_path=model_path)


BASE = os.path.dirname(os.path.abspath(__file__))

# 1. Bouncer Model (MobileNetV2 Leaf vs Non-Leaf Gate)
BOUNCER_MODEL_PATH = os.path.join(BASE, "model", "bouncer.tflite")
bouncer_interpreter = get_interpreter(BOUNCER_MODEL_PATH)
bouncer_interpreter.allocate_tensors()
bouncer_input_details = bouncer_interpreter.get_input_details()
bouncer_output_details = bouncer_interpreter.get_output_details()

# 2. Top 10 Major Indian Crops Classifier
INDIAN_MODEL_PATH = os.path.join(BASE, "model", "indian_crops.tflite")
INDIAN_CLASSES_PATH = os.path.join(BASE, "model", "indian_classes.json")

# Fallback to legacy model if indian_crops.tflite is still training
if os.path.exists(INDIAN_MODEL_PATH) and os.path.exists(INDIAN_CLASSES_PATH):
    PRIMARY_MODEL_PATH = INDIAN_MODEL_PATH
    with open(INDIAN_CLASSES_PATH, "r", encoding="utf-8") as f:
        CLASS_NAMES = json.load(f)
    IS_INDIAN_MODEL = True
else:
    PRIMARY_MODEL_PATH = os.path.join(BASE, "model", "model.tflite")
    with open(os.path.join(BASE, "model", "class_names.json"), "r", encoding="utf-8") as f:
        CLASS_NAMES = json.load(f)
    IS_INDIAN_MODEL = False

interpreter = get_interpreter(PRIMARY_MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(f"[OK] Classifier loaded -- {len(CLASS_NAMES)} classes ready ({'Indian Crops v2' if IS_INDIAN_MODEL else 'Legacy'}). Bouncer active.")

# ── Solutions database ─────────────────────────────────────────
SOLUTIONS = {
    # ── 1. Cotton ──────────────────────────────────────────────
    "Cotton___Bollworm": {
        "cause": "Insect pest — Helicoverpa armigera (Cotton/American Bollworm) / Pectinophora gossypiella (Pink Bollworm)",
        "symptoms": "Bored entry holes in flower buds and bolls plugged with dark frass pellets, dropped squares, larval chewing on leaves",
        "severity": "Severe",
        "organic_cure": "Install pheromone traps (5 traps/acre). Spray Bacillus thuringiensis (Bt) formulation @ 2g/L or 5% Neem Seed Kernel Extract (NSKE). Handpick visible larvae.",
        "chemical_cure": "Emamectin benzoate 5% SG @ 0.4g/L or Chlorantraniliprole 18.5% SC @ 0.3ml/L or Spinosad 45% SC @ 0.3ml/L",
        "prevention": "Deep summer plowing to expose pupae, grow marigold or castor trap crops on field borders, avoid excessive nitrogen",
        "recovery_time": "2-3 weeks — prompt control critical before bolls are penetrated"
    },
    "Cotton___Bacterial_Blight": {
        "cause": "Bacteria — Xanthomonas citri pv. malvacearum",
        "symptoms": "Angular dark brown to black water-soaked leaf spots delineated by veins, black arm lesions on stems and petioles",
        "severity": "Moderate to Severe",
        "organic_cure": "Copper hydroxide spray @ 2g/L, bio-fungicide seed treatment with Pseudomonas fluorescens @ 10g/kg",
        "chemical_cure": "Copper oxychloride 50% WP @ 2.5g/L + Streptocycline @ 0.1g/L (1g per 10L water)",
        "prevention": "Use acid-delinted certified disease-free seeds, avoid sprinkler irrigation, remove infected debris",
        "recovery_time": "3-4 weeks"
    },
    "Cotton___Curl_Virus": {
        "cause": "Virus — Cotton Leaf Curl Virus (CLCuD), transmitted by Whitefly (Bemisia tabaci)",
        "symptoms": "Upward or downward leaf curling, vein thickening and cup-like enations on leaf undersides, stunted bushy growth",
        "severity": "Severe",
        "organic_cure": "Install yellow sticky traps (10-15/acre) to trap whitefly vector. Spray Neem oil (10,000 ppm) @ 2ml/L.",
        "chemical_cure": "Vector control: Diafenthiuron 50% WP @ 1.2g/L or Imidacloprid 17.8% SL @ 0.5ml/L or Pyriproxyfen 10% EC @ 1ml/L",
        "prevention": "Grow CLCuD-resistant cotton varieties, eradicate weed hosts around fields, crop rotation",
        "recovery_time": "Focus is on vector suppression; infected foliage cannot be reversed"
    },
    "Cotton___Healthy": {
        "cause": "None — Healthy Cotton Plant",
        "symptoms": "Vibrant green broad leaves, uniform square development, clean bolls with no lesions or pest chew holes",
        "severity": "None",
        "organic_cure": "Continue balanced farmyard manure, vermicompost, and organic mulching",
        "chemical_cure": "No chemical application required",
        "prevention": "Maintain regular scheduled irrigation, balanced N-P-K nutrition, and weekly field scouting",
        "recovery_time": "Plant is healthy"
    },

    # ── 2. Rice ───────────────────────────────────────────────
    "Rice___Blast": {
        "cause": "Fungus — Magnaporthe oryzae (Pyricularia oryzae)",
        "symptoms": "Diamond-shaped or spindle-shaped lesions with grayish-white centers and reddish-brown borders; blackening of neck nodes",
        "severity": "Severe",
        "organic_cure": "Spray Pseudomonas fluorescens @ 10g/L, apply silica fertilizer to strengthen leaf cuticle, avoid excess nitrogen",
        "chemical_cure": "Tricyclazole 75% WP @ 0.6g/L or Isoprothiolane 40% EC @ 1.5ml/L or Kasugamycin 3% SL @ 2ml/L",
        "prevention": "Treat seeds with Tricyclazole @ 2g/kg, avoid excessive urea application, maintain continuous shallow water layer",
        "recovery_time": "3-4 weeks — neck blast can cause severe yield loss if untreated before heading"
    },
    "Rice___Brown_Spot": {
        "cause": "Fungus — Bipolaris oryzae (Cochliobolus miyabeanus)",
        "symptoms": "Small oval to circular dark brown spots resembling sesame seeds with yellow halos scattered uniformly across leaves and glumes",
        "severity": "Moderate",
        "organic_cure": "Correct soil nutrient deficiency, apply balanced potassium and zinc, treat seeds with Trichoderma viride @ 5g/kg",
        "chemical_cure": "Mancozeb 75% WP @ 2g/L or Propiconazole 25% EC @ 1ml/L at tillering and boot leaf stage",
        "prevention": "Soil testing and balanced NPK + micronutrient application, use clean certified seed",
        "recovery_time": "2-3 weeks"
    },
    "Rice___Bacterial_Blight": {
        "cause": "Bacteria — Xanthomonas oryzae pv. oryzae",
        "symptoms": "Water-soaked stripes on leaf margins turning wavy yellow then bleaching white, bacterial ooze beads on young lesions",
        "severity": "Severe",
        "organic_cure": "Drain excess floodwater from field, reduce excess nitrogen fertilizer, spray fresh cow dung extract (20%)",
        "chemical_cure": "Copper oxychloride 50% WP @ 2.5g/L + Streptocycline @ 0.1g/L (1g per 10L water)",
        "prevention": "Grow resistant cultivars (e.g. Swarna Sub1, Improved Samba Mahsuri), avoid clipping seedling tips at transplanting",
        "recovery_time": "3-4 weeks"
    },
    "Rice___Healthy": {
        "cause": "None",
        "symptoms": "Vibrant green erect tillers, uniform canopy, healthy golden-yellow panicles with clean grains",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Alternate wetting and drying (AWD) water management, balanced NPK application",
        "recovery_time": "Not applicable"
    },

    # ── 3. Sugarcane ──────────────────────────────────────────
    "Sugarcane___Red_Rot": {
        "cause": "Fungus — Colletotrichum falcatum",
        "symptoms": "Drying and yellowing of 3rd and 4th leaves from top, longitudinal reddening of cane interior with diagnostic white cross-bands, alcoholic sour odor",
        "severity": "Critical (Severe)",
        "organic_cure": "Uproot and burn diseased clumps immediately, treat seed setts with Trichoderma viride @ 10g/L",
        "chemical_cure": "Sett treatment with Carbendazim 50% WP @ 1g/L for 15 minutes before planting; no curative spray once inside stalk",
        "prevention": "Plant resistant varieties (e.g. Co 0238, Co 86032), practice 2-year crop rotation, avoid flood drainage across fields",
        "recovery_time": "Systemic stalk infection cannot be reversed — rogue out affected stools immediately"
    },
    "Sugarcane___Yellow_Leaf": {
        "cause": "Virus — Sugarcane Yellow Leaf Virus (SCYLV), transmitted by Sugarcane Aphid (Melanaphis sacchari)",
        "symptoms": "Prominent yellowing of midrib on 3rd to 6th leaves from top, spreading outward to the leaf blade, bunching of leaves at crown",
        "severity": "Moderate to Severe",
        "organic_cure": "Spray insecticidal soap or Neem oil (10,000 ppm) @ 2ml/L to suppress sugarcane aphids",
        "chemical_cure": "Vector control: Imidacloprid 17.8% SL @ 0.5ml/L or Thiamethoxam 25% WG @ 0.5g/L",
        "prevention": "Plant virus-free tissue-cultured or heat-treated seed cane (MHAT 52°C for 30 min), control aphid colonies",
        "recovery_time": "Focus is on vector control and clean seed cane for next ratoon"
    },
    "Sugarcane___Rust": {
        "cause": "Fungus — Puccinia melanocephala",
        "symptoms": "Elongated yellowish spots turning reddish-brown pustules on both surfaces of leaf blades, premature leaf drying",
        "severity": "Moderate",
        "organic_cure": "Remove heavily rusted lower leaves, ensure good field drainage and air movement",
        "chemical_cure": "Mancozeb 75% WP @ 2.5g/L or Propiconazole 25% EC @ 1ml/L at first appearance",
        "prevention": "Avoid planting susceptible varieties in rust-prone areas, avoid excessive nitrogen",
        "recovery_time": "2-3 weeks"
    },
    "Sugarcane___Healthy": {
        "cause": "None",
        "symptoms": "Sturdy erect thick green canes, healthy broad leaf blades with clean midribs and vigorous stooling",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Trash mulching, balanced application of nitrogen and potash, regular field inspection",
        "recovery_time": "Not applicable"
    },

    # ── 4. Wheat ──────────────────────────────────────────────
    "Wheat___Rust": {
        "cause": "Fungus — Puccinia striiformis (Yellow Rust) / Puccinia triticina (Brown Rust) / Puccinia graminis (Black Rust)",
        "symptoms": "Bright yellow-orange powdery pustules in stripes along leaf veins; or scattered orange-brown pustules on leaf blades",
        "severity": "Severe",
        "organic_cure": "Foliar spray of neem seed kernel extract (5%), destroy self-sown wheat plants and weed hosts",
        "chemical_cure": "Propiconazole 25% EC (Tilt) @ 1ml/L (200ml/acre) or Tebuconazole 25.9% EC @ 1ml/L immediately at first sign",
        "prevention": "Cultivate rust-resistant varieties (e.g. DBW 187, DBW 222, HD 3226), timely sowing in November",
        "recovery_time": "2-3 weeks — prompt spray critical to stop fungal sporulation before flag leaf infection"
    },
    "Wheat___Healthy": {
        "cause": "None",
        "symptoms": "Uniform green tillers, clean erect flag leaves, well-filled spikelets with golden awns and healthy grain",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Timely crown root irrigation and balanced NPK fertilization",
        "recovery_time": "Not applicable"
    },

    # ── 5. Maize ──────────────────────────────────────────────
    "Maize___Fall_Armyworm": {
        "cause": "Insect pest — Spodoptera frugiperda (Fall Armyworm)",
        "symptoms": "Window-paning on young leaves, ragged shot-hole feeding damage, moist sawdust-like frass packed in leaf whorl",
        "severity": "Severe",
        "organic_cure": "Handpick egg masses and larvae, apply neem cake into the leaf whorl, spray Nomuraea rileyi or Bt @ 2g/L",
        "chemical_cure": "Chlorantraniliprole 18.5% SC @ 0.4ml/L or Emamectin benzoate 5% SG @ 0.4g/L directed into the leaf whorl",
        "prevention": "Deep summer plowing, intercrop with cowpea or pulses, erect pheromone traps @ 5/acre",
        "recovery_time": "2-3 weeks if sprayed before larvae bore deep into the stem/cob"
    },
    "Maize___Blight_Rust": {
        "cause": "Fungus — Exserohilum turcicum (Northern Leaf Blight) or Puccinia sorghi (Common Rust)",
        "symptoms": "Long elliptical grayish-green cigar-shaped lesions or brick-red powdery pustules on foliage",
        "severity": "Moderate to Severe",
        "organic_cure": "Spray copper oxychloride @ 2.5g/L, remove lower diseased leaves to improve aeration",
        "chemical_cure": "Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1ml/L or Mancozeb 75% WP @ 2.5g/L",
        "prevention": "Plant resistant hybrid seeds, crop rotation with legumes, avoid high plant density",
        "recovery_time": "3-4 weeks"
    },
    "Maize___Healthy": {
        "cause": "None",
        "symptoms": "Robust dark green leaves, sturdy stalk, uniform tassel and ear development with no chew damage",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Balanced nitrogen application in split doses, maintain optimal soil moisture",
        "recovery_time": "Not applicable"
    },

    # ── 6. Chilli ─────────────────────────────────────────────
    "Chilli___Leaf_Curl": {
        "cause": "Begomovirus (Chilli Leaf Curl Virus) transmitted by Whitefly (Bemisia tabaci) or severe Thrips feeding",
        "symptoms": "Upward curling and puckering of leaves, vein thickening, stunted bushy plant growth",
        "severity": "Severe",
        "organic_cure": "Spray Neem oil (10,000 ppm) @ 2ml/L, install yellow and blue sticky traps (15-20/acre)",
        "chemical_cure": "Control whitefly/thrips vector: Diafenthiuron 50% WP @ 1.2g/L or Fipronil 5% SC @ 1.5ml/L or Imidacloprid 17.8% SL @ 0.5ml/L",
        "prevention": "Grow border crops (maize/sorghum) to block whiteflies, rogue out infected plants early",
        "recovery_time": "Vector control halts new spread; curled foliage cannot be reversed"
    },
    "Chilli___Anthracnose": {
        "cause": "Fungus — Colletotrichum capsici",
        "symptoms": "Circular sunken lesions on fruits with concentric rings of dark acervuli, die-back of twigs",
        "severity": "Severe",
        "organic_cure": "Spray 5% Neem Seed Kernel Extract (NSKE) or Trichoderma viride @ 5g/L",
        "chemical_cure": "Azoxystrobin 23% SC @ 1ml/L or Difenoconazole 25% EC @ 1ml/L or Mancozeb 75% WP @ 2.5g/L",
        "prevention": "Use disease-free certified seeds, treat seeds with Thiram @ 3g/kg, avoid overhead sprinkler irrigation",
        "recovery_time": "2-3 weeks"
    },
    "Chilli___Healthy": {
        "cause": "None",
        "symptoms": "Vigorous dark green foliage, abundant flowering and glossy green pods without spots",
        "severity": "None",
        "organic_cure": "Not required — continue vermicompost and balanced neem cake application",
        "chemical_cure": "Not required",
        "prevention": "Maintain regular drip irrigation and scout for sucking pests",
        "recovery_time": "Not applicable"
    },

    # ── 7. Mustard ────────────────────────────────────────────
    "Mustard___Blight_WhiteRust": {
        "cause": "Fungus — Alternaria brassicae (Blight) or Albugo candida (White Rust)",
        "symptoms": "Dark brown spots with concentric target rings on leaves and pods; raised white blister pustules on leaf undersides",
        "severity": "Moderate to Severe",
        "organic_cure": "Spray Trichoderma harzianum @ 5g/L or 5% Neem extract, remove infected lower leaves",
        "chemical_cure": "Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ) @ 2g/L or Iprodione 50% WP @ 2g/L",
        "prevention": "Timely sowing in mid-October to escape aphid/disease peak, clean cultivation, certified seeds",
        "recovery_time": "2-3 weeks"
    },
    "Mustard___Healthy": {
        "cause": "None",
        "symptoms": "Healthy broad green foliage, vigorous branching, vibrant yellow flower clusters and firm green siliquae (pods)",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Timely irrigation at flowering and pod development stages",
        "recovery_time": "Not applicable"
    },

    # ── 8. Soybean ────────────────────────────────────────────
    "Soybean___Diseased": {
        "cause": "Fungus / Bacteria — Phakopsora pachyrhizi (Rust) or Cercospora sojina (Frogeye) or Xanthomonas (Bacterial Blight)",
        "symptoms": "Small brown to reddish-brown lesions or pustules on leaves, circular tan spots with purple borders, premature leaf drop",
        "severity": "Moderate to Severe",
        "organic_cure": "Spray Pseudomonas fluorescens @ 5g/L, apply neem oil (5ml/L) at early vegetative stage",
        "chemical_cure": "Hexaconazole 5% EC @ 1.5ml/L or Pyraclostrobin 20% WG @ 1g/L or Carbendazim 12% + Mancozeb 63% WP @ 2g/L",
        "prevention": "Grow rust-tolerant varieties, avoid water stagnation, practice 2-year crop rotation with maize or sorghum",
        "recovery_time": "2-3 weeks"
    },
    "Soybean___Healthy": {
        "cause": "None",
        "symptoms": "Dense dark green trifoliate leaves, strong branching, abundant pod setting with clean green pods",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Maintain adequate soil moisture during pod filling stage, monitor for defoliating caterpillars",
        "recovery_time": "Not applicable"
    },

    # ── 9. Potato ─────────────────────────────────────────────
    "Potato___Blight": {
        "cause": "Oomycete / Fungus — Phytophthora infestans (Late Blight) or Alternaria solani (Early Blight)",
        "symptoms": "Water-soaked irregular dark lesions rapidly turning brown with white downy growth underneath in humid conditions",
        "severity": "Severe",
        "organic_cure": "Spray Bordeaux mixture (1%) or copper hydroxide @ 2g/L, remove blighted haulms before harvest",
        "chemical_cure": "Cymoxanil 8% + Mancozeb 64% WP @ 2.5g/L or Dimethomorph 50% WP @ 1g/L",
        "prevention": "Plant certified disease-free seed tubers, ensure high earthing-up to protect tubers, proper drainage",
        "recovery_time": "3-4 weeks — act immediately within 24 hours of first symptom"
    },
    "Potato___Healthy": {
        "cause": "None",
        "symptoms": "Lush green bushy canopy with no spotting, firm stems, healthy tuber development beneath soil",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Timely earthing-up, balanced potassium and phosphorus application",
        "recovery_time": "Not applicable"
    },

    # ── 10. Tomato ────────────────────────────────────────────
    "Tomato___Blight_LeafCurl": {
        "cause": "Oomycete / Fungus / Begomovirus — Phytophthora infestans (Late Blight) or Alternaria (Early Blight) or TYLCV",
        "symptoms": "Concentric dark target spots or water-soaked brown patches; upward curling, yellow margins and stunted crinkled growth",
        "severity": "Severe",
        "organic_cure": "Copper hydroxide spray @ 2g/L or Neem oil (10,000 ppm) @ 2ml/L, yellow sticky traps for whitefly control",
        "chemical_cure": "Metalaxyl 8% + Mancozeb 64% WP @ 2.5g/L for blights; Diafenthiuron 50% WP @ 1.2g/L for whitefly vector",
        "prevention": "Stake plants to keep foliage off ground, crop rotation, avoid wetting leaves during irrigation",
        "recovery_time": "2-3 weeks"
    },
    "Tomato___Healthy": {
        "cause": "None",
        "symptoms": "Deep green healthy compound leaves, strong branching, abundant blossoms and clean glossy fruit",
        "severity": "None",
        "organic_cure": "Not required",
        "chemical_cure": "Not required",
        "prevention": "Consistent drip irrigation, balanced calcium and potassium fertilization to prevent blossom end rot",
        "recovery_time": "Not applicable"
    },
}

def get_solution(class_name: str) -> dict:
    if class_name in SOLUTIONS:
        return SOLUTIONS[class_name]
    for key in SOLUTIONS:
        if key.lower() == class_name.lower():
            return SOLUTIONS[key]
    is_healthy = "healthy" in class_name.lower()
    return {
        "cause": "None" if is_healthy else "Consult local agricultural extension officer",
        "symptoms": "Plant appears healthy" if is_healthy else "Disease detected — expert consultation recommended",
        "severity": "None" if is_healthy else "Moderate",
        "organic_cure": "Not required" if is_healthy else "Spray 5% Neem extract, consult your local KVK office",
        "chemical_cure": "Not required" if is_healthy else "Consult your local KVK office",
        "prevention": "Continue good agricultural practices and regular monitoring",
        "recovery_time": "Not applicable" if is_healthy else "Consult local expert"
    }

def diagnose_crop(image_bytes: bytes, media_type: str = "image/jpeg") -> dict:
    try:
        # Preprocess base image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((224, 224))

        # --- 1) BOUNCER GATE (Leaf vs Non-Leaf Object Gate) ---
        # Bouncer model expects [0, 255] float32 input (preprocessing is built into model)
        bouncer_array = np.array(image, dtype=np.float32)
        bouncer_array = np.expand_dims(bouncer_array, axis=0)

        bouncer_interpreter.set_tensor(bouncer_input_details[0]['index'], bouncer_array)
        bouncer_interpreter.invoke()
        bouncer_pred = float(bouncer_interpreter.get_tensor(bouncer_output_details[0]['index'])[0][0])

        print(f"[DEBUG] Bouncer Leaf Probability: {bouncer_pred:.4f}")

        # If bouncer rejects as garbage/non-leaf, block immediately
        if bouncer_pred < 0.40:
            return {
                "error": "not_a_crop",
                "message": "We couldn't detect a clear leaf in this photo. Please try again."
            }

        # --- 2) TOP 10 INDIAN CROPS CLASSIFIER ---
        # Model expects [0, 255] float32 input (preprocessing is built into inference graph)
        crop_array = np.array(image, dtype=np.float32)
        crop_array = np.expand_dims(crop_array, axis=0)

        interpreter.set_tensor(input_details[0]['index'], crop_array)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])[0]

        top_idx = int(np.argmax(predictions))
        confidence = float(predictions[top_idx])
        class_name = CLASS_NAMES[top_idx]

        print(f"[DEBUG] Crop Classifier: {class_name} ({confidence:.2%})")

        # Out-of-Distribution Guard: If confidence < 40%, reject forced incorrect diagnosis
        if confidence < 0.40:
            return {
                "error": "not_a_crop",
                "message": "We detected plant foliage, but the symptoms do not match our recognized crops or pests. Please try a clearer close-up photo."
            }

        # Top 3 predictions
        top3_idx = np.argsort(predictions)[-3:][::-1]
        top3 = [
            {
                "disease": CLASS_NAMES[i].replace("___", " — ").replace("_", " "),
                "confidence": f"{predictions[i]:.1%}"
            }
            for i in top3_idx
        ]

        # Extract crop and disease
        parts = class_name.split("___")
        crop_name = parts[0].replace("_", " ").strip()
        raw_disease = parts[1] if len(parts) > 1 else class_name
        is_healthy = "healthy" in raw_disease.lower()
        disease_name = "Healthy" if is_healthy else raw_disease.replace("_", " ").title()

        solution = get_solution(class_name)

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
