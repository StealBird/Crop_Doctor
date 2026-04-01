import { useState, useRef, useEffect } from "react";
import { useLanguage, LANGUAGE_TO_API } from '../LanguageContext';
 
const API = process.env.REACT_APP_API_URL;
 
// Quick-suggestion chips per language
const SUGGESTIONS = {
  english: {
    healthy: ["How to maintain health?", "Suggest fertilizer", "Next season tips"],
    disease: ["Where to buy medicine?", "Any organic option?", "How many days to recover?", "What's the cost?"],
  },
  hindi: {
    healthy: ["स्वास्थ्य कैसे बनाए रखें?", "उर्वरक सुझाएं", "अगले सीजन के टिप्स"],
    disease: ["दवाई कहाँ मिलेगी?", "कोई जैविक उपाय?", "कितने दिन में ठीक होगा?", "खर्चा कितना आएगा?"],
  },
  marathi: {
    healthy: ["आरोग्य कसे राखावे?", "खत सुचवा", "पुढील हंगामाच्या टिप्स"],
    disease: ["औषध कुठे मिळेल?", "सेंद्रिय पर्याय आहे का?", "किती दिवसांत बरे होईल?", "खर्च किती येईल?"],
  },
  hinglish: {
    healthy: ["Health kaise maintain karein?", "Fertilizer suggest karo", "Next season tips do"],
    disease: ["Yeh dawai kahan milegi?", "Organic option hai?", "Kitne din mein theek hoga?", "Kharcha kitna aayega?"],
  },
};
 
// Intro messages per language
const INTRO = {
  english: { healthy: (crop) => `Your ${crop} is completely healthy! No disease detected. Ask me anything about how to keep it growing strong.`,
             disease: (crop, disease) => `Hello! I'm your Crop Doctor. I've detected ${disease} in your ${crop}. Don't worry — it's treatable. Ask me anything about treatment, cost, or prevention.` },
  hindi:   { healthy: (crop) => `आपका ${crop} पूरी तरह स्वस्थ है! कोई रोग नहीं मिला। इसे मजबूत रखने के लिए कुछ भी पूछें।`,
             disease: (crop, disease) => `नमस्ते! मैं आपका Crop Doctor हूं। आपके ${crop} में ${disease} मिला है। चिंता न करें — यह ठीक हो सकता है।` },
  marathi: { healthy: (crop) => `तुमचा ${crop} पूर्णपणे निरोगी आहे! कोणताही रोग आढळला नाही। त्याला मजबूत ठेवण्यासाठी काहीही विचारा.`,
             disease: (crop, disease) => `नमस्कार! मी तुमचा Crop Doctor आहे. तुमच्या ${crop} मध्ये ${disease} आढळला आहे. काळजी करू नका.` },
  hinglish:{ healthy: (crop) => `Tumhara ${crop} bilkul healthy hai! Koi bimari nahi mili. Ise strong rakhne ke liye kuch bhi puchho.`,
             disease: (crop, disease) => `Hello! Main tumhara Crop Doctor hoon. Tumhare ${crop} mein ${disease} mila hai. Tension mat lo — ye theek ho sakta hai.` },
};
 
// Error messages per language
const ERROR_MSG = {
  english:  "Something went wrong. Please try again.",
  hindi:    "कुछ समस्या आई। दोबारा कोशिश करें।",
  marathi:  "काहीतरी चूक झाली. पुन्हा प्रयत्न करा.",
  hinglish: "Thoda problem aa gaya. Phir try karein.",
};
 
// Placeholder per language
const PLACEHOLDER = {
  english:  "Ask anything about this disease...",
  hindi:    "इस रोग के बारे में कुछ भी पूछें...",
  marathi:  "या रोगाबद्दल काहीही विचारा...",
  hinglish: "Is bimari ke baare mein kuch bhi puchho...",
};
 
// Send button label per language
const SEND_LABEL = {
  english:  "Send",
  hindi:    "भेजें",
  marathi:  "पाठवा",
  hinglish: "Bhejo",
};
 
export default function ChatBox({ disease, crop, is_healthy }) {
  const { language } = useLanguage();
 
  const getIntro = (lang) => {
    const msgs = INTRO[lang] || INTRO.english;
    return is_healthy ? msgs.healthy(crop) : msgs.disease(crop, disease);
  };
 
  const [messages, setMessages] = useState([{ from: "ai", text: getIntro(language) }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
 
  // When the global language changes, add a language-switch notice in chat
  const prevLangRef = useRef(language);
  useEffect(() => {
    if (prevLangRef.current !== language) {
      prevLangRef.current = language;
      const notice = {
        english:  "Switched to English. Ask me anything!",
        hindi:    "हिंदी में बदल दिया। कुछ भी पूछो!",
        marathi:  "मराठीत बदलले. काहीही विचारा!",
        hinglish: "Hinglish mein switch kar diya. Kuch bhi poochho!",
      };
      setMessages(prev => [...prev, { from: "ai", text: notice[language] || notice.english }]);
    }
  }, [language]);
 
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
 
  const suggestions = (SUGGESTIONS[language] || SUGGESTIONS.english)[is_healthy ? "healthy" : "disease"];
 
  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { from: "user", text: userMsg }]);
    setLoading(true);
 
    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMsg,
          disease,
          crop,
          is_healthy,
          language: LANGUAGE_TO_API[language],   // ← uses global language
        }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { from: "ai", text: data.reply }]);
    } catch {
      setMessages(prev => [
        ...prev,
        { from: "ai", text: ERROR_MSG[language] || ERROR_MSG.english }
      ]);
    } finally {
      setLoading(false);
    }
  };
 
  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };
 
  return (
    <div className="rounded-2xl border border-green-200 bg-white shadow-sm overflow-hidden">
 
      {/* Header — no language dropdown here, it's in the App header now */}
      <div className="bg-green-700 px-4 py-3 flex items-center gap-2">
        <div className="w-2 h-2 bg-green-300 rounded-full animate-pulse"></div>
        <span className="text-white font-semibold text-sm">🌿 Crop Doctor — Live Chat</span>
      </div>
 
      {/* Messages */}
      <div className="p-4 space-y-3 max-h-72 overflow-y-auto bg-gray-50">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.from === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-xs px-4 py-2 rounded-2xl text-sm leading-relaxed ${
              msg.from === "ai"
                ? "bg-white border border-green-100 text-gray-800 rounded-tl-sm shadow-sm"
                : "bg-green-600 text-white rounded-tr-sm"
            }`}>
              {msg.from === "ai" && (
                <span className="text-green-600 font-semibold text-xs block mb-1">🌿 Crop Doctor</span>
              )}
              {msg.text}
            </div>
          </div>
        ))}
 
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-green-100 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
              <div className="flex gap-1">
                {[0,1,2].map(i => (
                  <div key={i} className="w-2 h-2 bg-green-400 rounded-full animate-bounce"
                    style={{ animationDelay: `${i * 0.15}s` }} />
                ))}
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
 
      {/* Quick suggestions */}
      <div className="px-3 py-2 flex gap-2 overflow-x-auto bg-gray-50 border-t border-gray-100">
        {suggestions.map((s, i) => (
          <button key={i} onClick={() => setInput(s)}
            className="flex-shrink-0 text-xs bg-green-50 text-green-700 border border-green-200 px-3 py-1 rounded-full hover:bg-green-100 transition-colors">
            {s}
          </button>
        ))}
      </div>
 
      {/* Input */}
      <div className="p-3 bg-white border-t border-gray-100 flex gap-2">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder={PLACEHOLDER[language] || PLACEHOLDER.english}
          className="flex-1 text-sm border border-gray-200 rounded-xl px-4 py-2 outline-none focus:border-green-400 focus:ring-1 focus:ring-green-400"
        />
        <button
          onClick={send}
          disabled={loading || !input.trim()}
          className="bg-green-600 hover:bg-green-700 disabled:opacity-40 text-white px-4 py-2 rounded-xl text-sm font-medium transition-colors min-w-16 text-center"
        >
          {SEND_LABEL[language] || SEND_LABEL.english}
        </button>
      </div>
    </div>
  );
}
