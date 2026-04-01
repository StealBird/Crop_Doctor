// ============================================================
// translations.js  —  Crop Doctor Language System
// All UI strings in: English | Hindi | Marathi | Hinglish
// Usage: t('key') returns the string for the current language
// ============================================================

const translations = {
  english: {
    // --- App Header ---
    app_title: "Crop Doctor",
    app_tagline: "AI-powered crop disease detection",
    language_label: "Language",

    // --- Upload / Camera Screen ---
    select_crop: "Select your crop",
    upload_photo: "Upload Photo",
    take_photo: "Take Photo",
    or: "or",
    upload_hint: "Take a clear photo of the diseased leaf",
    diagnose_button: "Diagnose Now",
    supported_crops: "Supported crops",

    // --- Loader ---
    loading_line1: "Analysing your crop...",
    loading_line2: "Running AI diagnosis...",
    loading_line3: "Almost ready...",

    // --- Result Card ---
    result_title: "Diagnosis Result",
    crop: "Crop",
    disease: "Disease",
    confidence: "Confidence",
    severity: "Severity",
    cause: "Cause",
    symptoms: "Symptoms",
    organic_cure: "Organic Treatment",
    chemical_cure: "Chemical Treatment",
    prevention: "Prevention",
    recovery_time: "Recovery Time",
    top_predictions: "Top Predictions",
    healthy_message: "Your crop looks healthy! 🌿",
    healthy_sub: "No disease detected. Keep up the good care.",
    severity_low: "Low",
    severity_medium: "Medium",
    severity_high: "High",

    // --- Chatbot ---
    ask_ai: "Ask AI Doctor",
    chat_placeholder: "Ask anything about this disease...",
    chat_send: "Send",
    chat_thinking: "AI Doctor is thinking...",
    chat_intro: "Hi! I'm your AI Doctor. Ask me anything about this diagnosis.",

    // --- Errors ---
    error_try_again: "Something went wrong. Please try again.",
    error_no_image: "Please select or take a photo first.",
    error_api_down: "Server is starting up. Please wait 30 seconds and try again.",

    // --- Buttons ---
    back_button: "← New Diagnosis",
    share_button: "Share Result",
  },

  hindi: {
    // --- App Header ---
    app_title: "Crop Doctor",
    app_tagline: "AI से फसल रोग पहचानें",
    language_label: "भाषा",

    // --- Upload / Camera Screen ---
    select_crop: "अपनी फसल चुनें",
    upload_photo: "फोटो अपलोड करें",
    take_photo: "फोटो खींचें",
    or: "या",
    upload_hint: "बीमार पत्ते की साफ फोटो लें",
    diagnose_button: "निदान करें",
    supported_crops: "समर्थित फसलें",

    // --- Loader ---
    loading_line1: "आपकी फसल की जांच हो रही है...",
    loading_line2: "AI निदान चल रहा है...",
    loading_line3: "लगभग तैयार...",

    // --- Result Card ---
    result_title: "निदान परिणाम",
    crop: "फसल",
    disease: "रोग",
    confidence: "सटीकता",
    severity: "गंभीरता",
    cause: "कारण",
    symptoms: "लक्षण",
    organic_cure: "जैविक उपचार",
    chemical_cure: "रासायनिक उपचार",
    prevention: "बचाव के उपाय",
    recovery_time: "ठीक होने का समय",
    top_predictions: "शीर्ष अनुमान",
    healthy_message: "आपकी फसल स्वस्थ दिखती है! 🌿",
    healthy_sub: "कोई रोग नहीं मिला। देखभाल जारी रखें।",
    severity_low: "कम",
    severity_medium: "मध्यम",
    severity_high: "अधिक",

    // --- Chatbot ---
    ask_ai: "AI डॉक्टर से पूछें",
    chat_placeholder: "इस रोग के बारे में कुछ भी पूछें...",
    chat_send: "भेजें",
    chat_thinking: "AI डॉक्टर सोच रहा है...",
    chat_intro: "नमस्ते! मैं आपका AI डॉक्टर हूं। इस निदान के बारे में कुछ भी पूछें।",

    // --- Errors ---
    error_try_again: "कुछ गलत हुआ। कृपया दोबारा कोशिश करें।",
    error_no_image: "पहले कोई फोटो चुनें या लें।",
    error_api_down: "सर्वर शुरू हो रहा है। 30 सेकंड रुकें और फिर कोशिश करें।",

    // --- Buttons ---
    back_button: "← नया निदान",
    share_button: "परिणाम शेयर करें",
  },

  marathi: {
    // --- App Header ---
    app_title: "Crop Doctor",
    app_tagline: "AI द्वारे पिकाचे रोग ओळखा",
    language_label: "भाषा",

    // --- Upload / Camera Screen ---
    select_crop: "तुमचे पिक निवडा",
    upload_photo: "फोटो अपलोड करा",
    take_photo: "फोटो काढा",
    or: "किंवा",
    upload_hint: "आजारी पानाचा स्पष्ट फोटो काढा",
    diagnose_button: "निदान करा",
    supported_crops: "समर्थित पिके",

    // --- Loader ---
    loading_line1: "तुमच्या पिकाची तपासणी होत आहे...",
    loading_line2: "AI निदान चालू आहे...",
    loading_line3: "जवळजवळ तयार...",

    // --- Result Card ---
    result_title: "निदान निकाल",
    crop: "पिक",
    disease: "रोग",
    confidence: "अचूकता",
    severity: "तीव्रता",
    cause: "कारण",
    symptoms: "लक्षणे",
    organic_cure: "सेंद्रिय उपचार",
    chemical_cure: "रासायनिक उपचार",
    prevention: "प्रतिबंध",
    recovery_time: "बरे होण्याची वेळ",
    top_predictions: "शीर्ष अंदाज",
    healthy_message: "तुमचे पिक निरोगी दिसते! 🌿",
    healthy_sub: "कोणताही रोग आढळला नाही. काळजी सुरू ठेवा.",
    severity_low: "कमी",
    severity_medium: "मध्यम",
    severity_high: "जास्त",

    // --- Chatbot ---
    ask_ai: "AI डॉक्टरला विचारा",
    chat_placeholder: "या रोगाबद्दल काहीही विचारा...",
    chat_send: "पाठवा",
    chat_thinking: "AI डॉक्टर विचार करत आहे...",
    chat_intro: "नमस्कार! मी तुमचा AI डॉक्टर आहे. या निदानाबद्दल काहीही विचारा.",

    // --- Errors ---
    error_try_again: "काहीतरी चुकले. कृपया पुन्हा प्रयत्न करा.",
    error_no_image: "आधी फोटो निवडा किंवा काढा.",
    error_api_down: "सर्व्हर सुरू होत आहे. ३० सेकंद थांबा आणि पुन्हा प्रयत्न करा.",

    // --- Buttons ---
    back_button: "← नवीन निदान",
    share_button: "निकाल शेअर करा",
  },

  hinglish: {
    // --- App Header ---
    app_title: "Crop Doctor",
    app_tagline: "AI se fasal ki bimari pakdo",
    language_label: "Language",

    // --- Upload / Camera Screen ---
    select_crop: "Apni fasal chuno",
    upload_photo: "Photo Upload Karo",
    take_photo: "Photo Lo",
    or: "ya",
    upload_hint: "Beemar patte ki saaf photo lo",
    diagnose_button: "Diagnose Karo",
    supported_crops: "Supported fasalein",

    // --- Loader ---
    loading_line1: "Aapki fasal check ho rahi hai...",
    loading_line2: "AI diagnosis chal rahi hai...",
    loading_line3: "Bilkul ready hone wala hai...",

    // --- Result Card ---
    result_title: "Diagnosis Result",
    crop: "Fasal",
    disease: "Bimari",
    confidence: "Accuracy",
    severity: "Gambhirta",
    cause: "Karan",
    symptoms: "Lakshan",
    organic_cure: "Jaivik Ilaj",
    chemical_cure: "Chemical Ilaj",
    prevention: "Bachav ke Tarike",
    recovery_time: "Theek Hone Ka Time",
    top_predictions: "Top Predictions",
    healthy_message: "Aapki fasal healthy hai! 🌿",
    healthy_sub: "Koi bimari nahi mili. Aise hi dekhbhal karte raho.",
    severity_low: "Kam",
    severity_medium: "Theek-Theek",
    severity_high: "Zyada",

    // --- Chatbot ---
    ask_ai: "AI Doctor Se Puchho",
    chat_placeholder: "Is bimari ke baare mein kuch bhi puchho...",
    chat_send: "Bhejo",
    chat_thinking: "AI Doctor soch raha hai...",
    chat_intro: "Hello! Main aapka AI Doctor hoon. Is diagnosis ke baare mein kuch bhi puchho.",

    // --- Errors ---
    error_try_again: "Kuch galat hua. Dobara try karo.",
    error_no_image: "Pehle koi photo chuno ya lo.",
    error_api_down: "Server shuru ho raha hai. 30 second ruko aur dobara try karo.",

    // --- Buttons ---
    back_button: "← Naya Diagnosis",
    share_button: "Result Share Karo",
  },
};

export default translations;
