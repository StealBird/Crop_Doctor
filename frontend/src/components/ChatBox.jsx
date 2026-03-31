import { useState, useRef, useEffect } from "react";

const API = process.env.REACT_APP_API_URL;

const LANGUAGES = {
  EN: { label: "English", send: "Send", placeholder: "Ask anything...", code: "english" },
  HI: { label: "हिंदी", send: "भेजो", placeholder: "कुछ भी पूछो...", code: "hindi" },
  MR: { label: "मराठी", send: "पाठवा", placeholder: "काहीही विचारा...", code: "marathi" },
  HL: { label: "Hinglish", send: "Bhejo", placeholder: "Kuch bhi poochho...", code: "hinglish" },
};

export default function ChatBox({ disease, crop, is_healthy }) {
  const [lang, setLang] = useState("EN");
  const [showLangMenu, setShowLangMenu] = useState(false);
  const [messages, setMessages] = useState([
    {
      from: "ai",
      text: is_healthy
        ? `Your ${crop} is completely healthy! No disease detected. Ask me anything about how to keep it growing strong.`
        : `Hello! I'm your Crop Doctor. I've detected ${disease} in your ${crop}. Don't worry — it's treatable. Ask me anything about treatment, cost, or prevention.`
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const langRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    const handleClick = (e) => {
      if (langRef.current && !langRef.current.contains(e.target)) {
        setShowLangMenu(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const currentLang = LANGUAGES[lang];

  const suggestions = {
    EN: is_healthy
      ? ["How to maintain health?", "Suggest fertilizer", "Next season tips"]
      : ["Where to buy medicine?", "Any organic option?", "How many days to recover?", "What's the cost?"],
    HI: is_healthy
      ? ["स्वास्थ्य कैसे बनाए रखें?", "उर्वरक सुझाएं", "अगले सीजन के टिप्स"]
      : ["दवाई कहाँ मिलेगी?", "कोई जैविक उपाय?", "कितने दिन में ठीक होगा?", "खर्चा कितना आएगा?"],
    MR: is_healthy
      ? ["आरोग्य कसे राखावे?", "खत सुचवा", "पुढील हंगामाच्या टिप्स"]
      : ["औषध कुठे मिळेल?", "सेंद्रिय पर्याय आहे का?", "किती दिवसांत बरे होईल?", "खर्च किती येईल?"],
    HL: is_healthy
      ? ["Health kaise maintain karein?", "Fertilizer suggest karo", "Next season tips do"]
      : ["Yeh dawai kahan milegi?", "Organic option hai?", "Kitne din mein theek hoga?", "Kharcha kitna aayega?"],
  };

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
          language: currentLang.code,
        }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { from: "ai", text: data.reply }]);
    } catch {
      setMessages(prev => [
        ...prev,
        { from: "ai", text: lang === "HI" ? "कुछ समस्या आई। दोबारा कोशिश करें।" : lang === "MR" ? "काहीतरी चूक झाली. पुन्हा प्रयत्न करा." : lang === "HL" ? "Thoda problem aa gaya. Phir try karein." : "Something went wrong. Please try again." }
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

  const selectLang = (code) => {
    setLang(code);
    setShowLangMenu(false);
    // Add a language switch message
    const switchMsg = {
      EN: "Switched to English. Ask me anything!",
      HI: "हिंदी में बदल दिया। कुछ भी पूछो!",
      MR: "मराठीत बदलले. काहीही विचारा!",
      HL: "Hinglish mein switch kar diya. Kuch bhi poochho!",
    };
    setMessages(prev => [...prev, { from: "ai", text: switchMsg[code] }]);
  };

  return (
    <div className="rounded-2xl border border-green-200 bg-white shadow-sm overflow-hidden">

      {/* Header with language selector */}
      <div className="bg-green-700 px-4 py-3 flex items-center gap-2">
        <div className="w-2 h-2 bg-green-300 rounded-full animate-pulse"></div>
        <span className="text-white font-semibold text-sm">Crop Doctor — Live Chat</span>

        {/* Language selector */}
        <div className="ml-auto relative" ref={langRef}>
          <button
            onClick={() => setShowLangMenu(!showLangMenu)}
            className="flex items-center gap-1 bg-green-600 hover:bg-green-500 text-white text-xs px-3 py-1.5 rounded-lg transition-colors"
          >
            <span>{currentLang.label}</span>
            <span className="text-green-300">▾</span>
          </button>

          {showLangMenu && (
            <div className="absolute right-0 top-8 bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden z-50 min-w-32">
              {Object.entries(LANGUAGES).map(([code, l]) => (
                <button
                  key={code}
                  onClick={() => selectLang(code)}
                  className={`w-full text-left px-4 py-2.5 text-sm transition-colors ${
                    lang === code
                      ? "bg-green-50 text-green-700 font-semibold"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  {l.label}
                </button>
              ))}
            </div>
          )}
        </div>
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
        {(suggestions[lang] || suggestions.EN).map((s, i) => (
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
          placeholder={currentLang.placeholder}
          className="flex-1 text-sm border border-gray-200 rounded-xl px-4 py-2 outline-none focus:border-green-400 focus:ring-1 focus:ring-green-400"
        />
        <button
          onClick={send}
          disabled={loading || !input.trim()}
          className="bg-green-600 hover:bg-green-700 disabled:opacity-40 text-white px-4 py-2 rounded-xl text-sm font-medium transition-colors min-w-16 text-center"
        >
          {currentLang.send}
        </button>
      </div>
    </div>
  );
}