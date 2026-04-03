// ============================================================
// translations.js  —  Crop Doctor Language System
// Keys used by: EN | HI | MR | HL
// t('key') / t('key', { crop: 'Tomato', disease: 'Blight' })
// ============================================================

const translations = {
  EN: {
    // ── Header ──
    app_title:     'Crop Doctor',
    app_tagline:   'AI Disease Detection',
    diagnose_title: 'Diagnose your crop.',
    diagnose_italic:'Instantly.',
    diagnose_sub:   '38 diseases · 14 crops · Free for every farmer',
    language_label:'Language',

    // ── Camera / Upload screen ──
    take_photo:     'Tap to take photo',
    upload_hint:    'Point camera at the affected leaf · or drag & drop',
    photo_selected: 'Photo selected — tap Diagnose to analyse',
    upload_photo:   'Upload from gallery',
    diagnose_button:'Diagnose this crop',
    supported_crops:'Supported crops — 38 diseases detected',
    select_crop:    'Select your crop',

    // ── Loader ──
    loading_line1: 'Analysing your crop...',
    loading_line2: 'AI is examining the leaf',
    loading_line3: 'Almost ready...',

    // ── Result Card ──
    result_title:    'Diagnosis Result',
    crop:            'Crop',
    disease:         'Disease',
    confidence:      'confidence',
    severity:        'Severity',
    cause:           'Cause',
    symptoms:        'Symptoms',
    organic_cure:    'Organic Treatment',
    chemical_cure:   'Chemical Treatment',
    prevention:      'Prevention',
    recovery_time:   'Recovery Time',
    top_predictions: 'Top predictions',
    healthy_message: 'Your crop looks healthy! 🌿',
    healthy_sub:     'No disease detected. Keep up the good care.',
    great_news:      'Great news!',
    diagnose_another:'Diagnose another crop',
    back_button:     '← New Diagnosis',
    share_button:    'Share Result',

    // ── Chat ──
    chat_title:       'Crop Doctor — Live Chat',
    chat_placeholder: 'Ask anything about this disease...',
    send_btn:         'Send',
    chat_send:        'Send',
    chat_healthy:     'Your {crop} is completely healthy! Ask me anything about keeping it strong.',
    chat_disease:     "Hello! I've detected {disease} in your {crop}. Don't worry — it's treatable. Ask anything!",
    chat_error:       'Something went wrong. Please try again.',
    lang_switched:    'Switched to English. Ask me anything!',
    chat_intro:       "Hi! I'm your AI Doctor. Ask me anything about this diagnosis.",
    ask_ai:           'Ask AI Doctor',
    chat_thinking:    'AI Doctor is thinking...',

    // ── Quick suggestions — healthy ──
    sug_maintain:   'How to maintain health?',
    sug_fertilizer: 'Suggest fertilizer',
    sug_next_season:'Next season tips',
    // ── Quick suggestions — diseased ──
    sug_buy:   'Where to buy medicine?',
    sug_organic:'Any organic option?',
    sug_days:  'How many days to recover?',
    sug_cost:  "What's the cost?",

    // ── Errors ──
    error_connect:  'Cannot connect to server. Please try again in a moment.',
    error_try_again:'Something went wrong. Please try again.',
    error_no_image: 'Please select or take a photo first.',
    error_api_down: 'Server is starting up. Please wait 30 seconds and try again.',
    error_not_crop: 'Please upload a clear photo of your crop or plant leaf. Non-crop images cannot be diagnosed.',
    try_again:      'Try Again',

    // ── Footer ──
    footer: 'Crop Doctor v1.0 — Free for every farmer',
    // ── Stat pills + FAB ──
    stat_crops:      '14 Crops',
    stat_diseases:   '38 Diseases',
    stat_ai:         'AI Specialist',
    ai_specialist_btn: 'AI Specialist',
    // ── Conversational chat ──
    conv_welcome:        'Welcome to Crop Doctor! 👋 Tap 📸 to upload a crop leaf photo for instant diagnosis, or ask me anything about crop diseases.',
    conv_thinking_crop:  'Analyzing your crop... 🌱',
    conv_thinking_chat:  'Thinking...',
    conv_analyzing:      'Analyzing this photo...',
    conv_show_details:   '▼ Show treatment',
    conv_hide_details:   '▲ Hide details',
  },

  HI: {
    // ── Header ──
    app_title:     'क्रॉप डॉक्टर',
    app_tagline:   'AI रोग पहचान',
    diagnose_title: 'अपनी फसल की जांच करें।',
    diagnose_italic:'तुरंत।',
    diagnose_sub:   '38 बीमारियाँ · 14 फसलें · हर किसान के लिए मुफ्त',
    language_label:'भाषा',

    // ── Camera / Upload screen ──
    take_photo:     'फोटो लेने के लिए टैप करें',
    upload_hint:    'कैमरा प्रभावित पत्ती पर रखें · या यहाँ खींचें',
    photo_selected: 'फोटो चुनी गई — जांच करने के लिए टैप करें',
    upload_photo:   'गैलरी से अपलोड करें',
    diagnose_button:'इस फसल की जांच करें',
    supported_crops:'समर्थित फसलें — 38 रोग पहचाने जाते हैं',
    select_crop:    'अपनी फसल चुनें',

    // ── Loader ──
    loading_line1: 'आपकी फसल की जांच हो रही है...',
    loading_line2: 'AI पत्ती की जांच कर रहा है',
    loading_line3: 'लगभग तैयार...',

    // ── Result Card ──
    result_title:    'निदान परिणाम',
    crop:            'फसल',
    disease:         'रोग',
    confidence:      'विश्वास',
    severity:        'गंभीरता',
    cause:           'कारण',
    symptoms:        'लक्षण',
    organic_cure:    'जैविक उपचार',
    chemical_cure:   'रासायनिक उपचार',
    prevention:      'रोकथाम',
    recovery_time:   'ठीक होने का समय',
    top_predictions: 'शीर्ष अनुमान',
    healthy_message: 'आपकी फसल स्वस्थ दिखती है! 🌿',
    healthy_sub:     'कोई रोग नहीं मिला। देखभाल जारी रखें।',
    great_news:      'बहुत अच्छी खबर!',
    diagnose_another:'दूसरी फसल की जांच करें',
    back_button:     '← नया निदान',
    share_button:    'परिणाम शेयर करें',

    // ── Chat ──
    chat_title:       'क्रॉप डॉक्टर — लाइव चैट',
    chat_placeholder: 'कुछ भी पूछो...',
    send_btn:         'भेजो',
    chat_send:        'भेजें',
    chat_healthy:     'आपका {crop} बिल्कुल स्वस्थ है! इसे मजबूत रखने के बारे में कुछ भी पूछें।',
    chat_disease:     'नमस्ते! आपके {crop} में {disease} पाया गया है। घबराएं नहीं — यह ठीक हो सकता है!',
    chat_error:       'कुछ गलत हो गया। कृपया फिर से कोशिश करें।',
    lang_switched:    'हिंदी में बदल दिया। कुछ भी पूछो!',
    chat_intro:       'नमस्ते! मैं आपका AI डॉक्टर हूं। इस निदान के बारे में कुछ भी पूछें।',
    ask_ai:           'AI डॉक्टर से पूछें',
    chat_thinking:    'AI डॉक्टर सोच रहा है...',

    // ── Quick suggestions — healthy ──
    sug_maintain:   'स्वास्थ्य कैसे बनाए रखें?',
    sug_fertilizer: 'उर्वरक सुझाएं',
    sug_next_season:'अगले सीज़न की टिप्स',
    // ── Quick suggestions — diseased ──
    sug_buy:    'दवाई कहाँ मिलेगी?',
    sug_organic:'कोई जैविक उपाय?',
    sug_days:   'कितने दिन में ठीक होगा?',
    sug_cost:   'खर्चा कितना आएगा?',

    // ── Errors ──
    error_connect:  'सर्वर से कनेक्ट नहीं हो पाया। थोड़ी देर बाद फिर कोशिश करें।',
    error_try_again:'कुछ गलत हुआ। कृपया दोबारा कोशिश करें।',
    error_no_image: 'पहले कोई फोटो चुनें या लें।',
    error_api_down: 'सर्वर शुरू हो रहा है। 30 सेकंड रुकें और फिर कोशिश करें।',
    error_not_crop: 'कृपया अपनी फसल या पत्ती की साफ फोटो अपलोड करें। यह फसल की फोटो नहीं है।',
    try_again:      'फिर कोशिश करें',

    // ── Footer ──
    footer: 'क्रॉप डॉक्टर v1.0 — हर किसान के लिए मुफ्त',
    // ── Stat pills + FAB ──
    stat_crops:      '14 फसलें',
    stat_diseases:   '38 बीमारियाँ',
    stat_ai:         'AI विशेषज्ञ',
    ai_specialist_btn: 'AI विशेषज्ञ',
    // ── Conversational chat ──
    conv_welcome:        'Crop Doctor में आपका स्वागत है! 👋 तत्काल निदान के लिए 📸 टैप करें, या फसल रोगों के बारे में कुछ भी पूछें।',
    conv_thinking_crop:  'आपकी फसल की जांच हो रही है... 🌱',
    conv_thinking_chat:  'सोच रहा हूँ...',
    conv_analyzing:      'इस फोटो की जांच हो रही है...',
    conv_show_details:   '▼ उपचार दिखाएं',
    conv_hide_details:   '▲ छुपाएं',
  },

  MR: {
    // ── Header ──
    app_title:     'क्रॉप डॉक्टर',
    app_tagline:   'AI रोग शोध',
    diagnose_title: 'आपल्या पिकाची तपासणी करा।',
    diagnose_italic:'तत्काळ।',
    diagnose_sub:   '38 रोग · 14 पिके · प्रत्येक शेतकऱ्यासाठी मोफत',
    language_label:'भाषा',

    // ── Camera / Upload screen ──
    take_photo:     'फोटो काढण्यासाठी टॅप करा',
    upload_hint:    'कॅमेरा बाधित पानावर धरा · किंवा इथे ड्रॅग करा',
    photo_selected: 'फोटो निवडला — तपासणीसाठी टॅप करा',
    upload_photo:   'गॅलरीतून अपलोड करा',
    diagnose_button:'हे पीक तपासा',
    supported_crops:'समर्थित पिके — 38 रोग ओळखले जातात',
    select_crop:    'तुमचे पिक निवडा',

    // ── Loader ──
    loading_line1: 'तुमच्या पिकाची तपासणी होत आहे...',
    loading_line2: 'AI पान तपासत आहे',
    loading_line3: 'जवळजवळ तयार...',

    // ── Result Card ──
    result_title:    'निदान निकाल',
    crop:            'पिक',
    disease:         'रोग',
    confidence:      'विश्वास',
    severity:        'तीव्रता',
    cause:           'कारण',
    symptoms:        'लक्षणे',
    organic_cure:    'सेंद्रिय उपचार',
    chemical_cure:   'रासायनिक उपचार',
    prevention:      'प्रतिबंध',
    recovery_time:   'बरे होण्याचा वेळ',
    top_predictions: 'शीर्ष अंदाज',
    healthy_message: 'तुमचे पिक निरोगी दिसते! 🌿',
    healthy_sub:     'कोणताही रोग आढळला नाही. काळजी सुरू ठेवा.',
    great_news:      'खूप छान बातमी!',
    diagnose_another:'दुसऱ्या पिकाची तपासणी करा',
    back_button:     '← नवीन निदान',
    share_button:    'निकाल शेअर करा',

    // ── Chat ──
    chat_title:       'क्रॉप डॉक्टर — लाइव्ह चॅट',
    chat_placeholder: 'काहीही विचारा...',
    send_btn:         'पाठवा',
    chat_send:        'पाठवा',
    chat_healthy:     'तुमचे {crop} पूर्णपणे निरोगी आहे! ते मजबूत ठेवण्याबद्दल काहीही विचारा।',
    chat_disease:     'नमस्कार! तुमच्या {crop} मध्ये {disease} आढळला आहे. घाबरू नका — हे बरे होऊ शकते!',
    chat_error:       'काहीतरी चूक झाली. पुन्हा प्रयत्न करा.',
    lang_switched:    'मराठीत बदलले. काहीही विचारा!',
    chat_intro:       'नमस्कार! मी तुमचा AI डॉक्टर आहे. या निदानाबद्दल काहीही विचारा.',
    ask_ai:           'AI डॉक्टरला विचारा',
    chat_thinking:    'AI डॉक्टर विचार करत आहे...',

    // ── Quick suggestions — healthy ──
    sug_maintain:   'आरोग्य कसे राखावे?',
    sug_fertilizer: 'खत सुचवा',
    sug_next_season:'पुढील हंगामाच्या टिप्स',
    // ── Quick suggestions — diseased ──
    sug_buy:    'औषध कुठे मिळेल?',
    sug_organic:'सेंद्रिय पर्याय आहे का?',
    sug_days:   'किती दिवसांत बरे होईल?',
    sug_cost:   'खर्च किती येईल?',

    // ── Errors ──
    error_connect:  'सर्व्हरशी कनेक्ट होता आले नाही. थोड्या वेळाने पुन्हा प्रयत्न करा.',
    error_try_again:'काहीतरी चुकले. कृपया पुन्हा प्रयत्न करा.',
    error_no_image: 'आधी फोटो निवडा किंवा काढा.',
    error_api_down: 'सर्व्हर सुरू होत आहे. ३० सेकंद थांबा आणि पुन्हा प्रयत्न करा.',
    error_not_crop: 'कृपया तुमच्या पिकाच्या किंवा पानाच्या स्पष्ट फोटो अपलोड करा. हे पीक नाही.',
    try_again:      'पुन्हा प्रयत्न करा',

    // ── Footer ──
    footer: 'क्रॉप डॉक्टर v1.0 — प्रत्येक शेतकऱ्यासाठी मोफत',
    // ── Stat pills + FAB ──
    stat_crops:      '14 पिके',
    stat_diseases:   '38 रोग',
    stat_ai:         'AI तज्ञ',
    ai_specialist_btn: 'AI तज्ञ',
    // ── Conversational chat ──
    conv_welcome:        'Crop Doctor मध्ये स्वागत आहे! 👋 तात्काळ निदानासाठी 📸 टॅप करा, किंवा पिकाच्या रोगांबद्दल काहीही विचारा.',
    conv_thinking_crop:  'तुमच्या पिकाची तपासणी होत आहे... 🌱',
    conv_thinking_chat:  'विचार करत आहे...',
    conv_analyzing:      'या फोटोची तपासणी होत आहे...',
    conv_show_details:   '▼ उपचार दाखवा',
    conv_hide_details:   '▲ लपवा',
  },

  HL: {
    // ── Header ──
    app_title:     'Crop Doctor',
    app_tagline:   'AI Bimari Pehchaan',
    diagnose_title: 'Apni fasal ki jaanch karo.',
    diagnose_italic:'Turant.',
    diagnose_sub:   '38 bimariyan · 14 faslen · Har kisan ke liye muft',
    language_label:'Language',

    // ── Camera / Upload screen ──
    take_photo:     'Photo lene ke liye tap karo',
    upload_hint:    'Camera bimaar patte par rakhein · ya yahan drag karein',
    photo_selected: 'Photo chuni gayi — Diagnose karne ke liye tap karo',
    upload_photo:   'Gallery se upload karo',
    diagnose_button:'Is fasal ki jaanch karo',
    supported_crops:'Supported faslen — 38 bimariyan pehchani jaati hain',
    select_crop:    'Apni fasal chuno',

    // ── Loader ──
    loading_line1: 'Aapki fasal ki jaanch ho rahi hai...',
    loading_line2: 'AI patta dekh raha hai',
    loading_line3: 'Bilkul ready hone wala hai...',

    // ── Result Card ──
    result_title:    'Diagnosis Result',
    crop:            'Fasal',
    disease:         'Bimari',
    confidence:      'Vishwaas',
    severity:        'Gambhirta',
    cause:           'Karan',
    symptoms:        'Lakshan',
    organic_cure:    'Jaivik Upchaar',
    chemical_cure:   'Rasaynik Upchaar',
    prevention:      'Roktham',
    recovery_time:   'Theek hone ka samay',
    top_predictions: 'Top Andaaze',
    healthy_message: 'Aapki fasal healthy hai! 🌿',
    healthy_sub:     'Koi bimari nahi mili. Aise hi dekhbhal karte raho.',
    great_news:      'Bahut achhi khabar!',
    diagnose_another:'Doosri fasal ki jaanch karo',
    back_button:     '← Naya Diagnosis',
    share_button:    'Result Share Karo',

    // ── Chat ──
    chat_title:       'Crop Doctor — Live Chat',
    chat_placeholder: 'Kuch bhi poochho...',
    send_btn:         'Bhejo',
    chat_send:        'Bhejo',
    chat_healthy:     'Aapka {crop} bilkul theek hai! Isko strong rakhne ke baare mein kuch bhi poochho.',
    chat_disease:     'Namaste! Aapke {crop} mein {disease} mili hai. Ghabrao mat — yeh theek ho sakti hai!',
    chat_error:       'Thoda problem aa gaya. Phir se try karein.',
    lang_switched:    'Hinglish mein switch kar diya. Kuch bhi poochho!',
    chat_intro:       'Hello! Main aapka AI Doctor hoon. Is diagnosis ke baare mein kuch bhi puchho.',
    ask_ai:           'AI Doctor Se Puchho',
    chat_thinking:    'AI Doctor soch raha hai...',

    // ── Quick suggestions — healthy ──
    sug_maintain:   'Health kaise maintain karein?',
    sug_fertilizer: 'Fertilizer suggest karo',
    sug_next_season:'Next season tips do',
    // ── Quick suggestions — diseased ──
    sug_buy:    'Yeh dawai kahan milegi?',
    sug_organic:'Organic option hai?',
    sug_days:   'Kitne din mein theek hoga?',
    sug_cost:   'Kharcha kitna aayega?',

    // ── Errors ──
    error_connect:  'Server se connect nahi hua. Thodi der baad try karein.',
    error_try_again:'Kuch galat hua. Dobara try karo.',
    error_no_image: 'Pehle koi photo chuno ya lo.',
    error_api_down: 'Server shuru ho raha hai. 30 second ruko aur dobara try karo.',
    error_not_crop: 'Kripya apni fasal ya patte ki clear photo upload karo. Yeh fasal ki photo nahi lag rahi.',
    try_again:      'Phir try karo',

    // ── Footer ──
    footer: 'Crop Doctor v1.0 — Har kisan ke liye muft',
    // ── Stat pills + FAB ──
    stat_crops:      '14 Faslen',
    stat_diseases:   '38 Bimariyan',
    stat_ai:         'AI Specialist',
    ai_specialist_btn: 'AI Specialist',
    // ── Conversational chat ──
    conv_welcome:        'Crop Doctor mein aapka swagat hai! 👋 Turant diagnosis ke liye 📸 tap karo, ya fasal bimariyon ke baare mein kuch bhi poochho.',
    conv_thinking_crop:  'Aapki fasal check ho rahi hai... 🌱',
    conv_thinking_chat:  'Soch raha hai...',
    conv_analyzing:      'Yeh photo check ho rahi hai...',
    conv_show_details:   '▼ Treatment dikhao',
    conv_hide_details:   '▲ Chhupao',
  },
};

export default translations;
