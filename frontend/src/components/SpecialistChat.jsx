import { useState, useRef, useEffect } from "react";
import { useLanguage } from '../LanguageContext';

const API = process.env.REACT_APP_API_URL;

// Maps new short codes (EN/HI/MR/HL) to the legacy keys used in local lookup objects
const LANG_CODE_MAP = { EN: 'english', HI: 'hindi', MR: 'marathi', HL: 'hinglish' };

const SPECIALIST_INTROS = {
  english: `👋 Hello! I'm **Dr. Agro AI**, your dedicated crop disease specialist. I'm here to help with any farming questions — disease prevention, soil health, pesticide advice, and treatment plans. What can I help you with today?`,
  hindi: `👋 नमस्ते! मैं **Dr. Agro AI** हूं, आपका विशेष फसल रोग विशेषज्ञ। मैं रोग नियंत्रण, मिट्टी की सेहत और उपचार योजना में मदद कर सकता हूं। आज क्या पूछना है?`,
  marathi: `👋 नमस्कार! मी **Dr. Agro AI** आहे, तुमचा पिक रोग तज्ञ. मी रोग प्रतिबंध, माती आरोग्य आणि उपचार योजनांमध्ये मदत करतो. आज काय विचारायचे आहे?`,
  hinglish: `👋 Hello! Main **Dr. Agro AI** hoon, tumhara dedicated crop disease specialist. Farming ke kisi bhi sawaal mein madad karunga — bimari, khaad, mitti, ya dawai. Aaj kya poochna hai?`,
};

const QUICK_ACTIONS = {
  english: [
    "Best fertilizer for wheat?",
    "How to prevent fungal disease?",
    "Organic pesticide options",
    "Soil pH problems",
    "Irrigation tips",
    "Seasonal crop advice",
  ],
  hindi: [
    "गेहूं के लिए बेस्ट खाद?",
    "फंगल रोग कैसे रोकें?",
    "जैविक कीटनाशक?",
    "मिट्टी pH की समस्या",
    "सिंचाई के टिप्स",
    "मौसमी फसल सलाह",
  ],
  marathi: [
    "गव्हासाठी उत्तम खत?",
    "बुरशीजन्य रोग कसे थांबवायचे?",
    "सेंद्रिय कीटकनाशक?",
    "मातीच्या pH समस्या",
    "सिंचन टिप्स",
    "हंगामी पिक सल्ला",
  ],
  hinglish: [
    "Gehun ke liye best khaad?",
    "Fungal bimari kaise rokein?",
    "Organic keetnashak?",
    "Mitti pH ki problem",
    "Sinchaai ke tips",
    "Seasonal fasal salah",
  ],
};

const PLACEHOLDER = {
  english:  "Ask any farming or crop health question...",
  hindi:    "खेती या फसल स्वास्थ्य के बारे में कुछ भी पूछें...",
  marathi:  "शेती किंवा पिक आरोग्याबद्दल काहीही विचारा...",
  hinglish: "Kheti ya fasal ke baare mein kuch bhi puchho...",
};

const ERROR_MSG = {
  english:  "Connection issue. Please try again.",
  hindi:    "कनेक्शन समस्या। दोबारा कोशिश करें।",
  marathi:  "कनेक्शन समस्या. पुन्हा प्रयत्न करा.",
  hinglish: "Connection problem. Phir try karo.",
};

export default function SpecialistChat({ onClose }) {
  const { lang, langCode } = useLanguage();

  const getIntro = (l) => SPECIALIST_INTROS[LANG_CODE_MAP[l]] || SPECIALIST_INTROS.english;

  const [messages, setMessages] = useState([
    { from: "ai", text: getIntro(lang) }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const inputRef  = useRef(null);

  // Regenerate greeting when language changes
  useEffect(() => {
    setMessages([{ from: "ai", text: getIntro(lang) }]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lang]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const send = async (text) => {
    const userMsg = (text || input).trim();
    if (!userMsg || loading) return;
    setInput("");
    setMessages(prev => [...prev, { from: "user", text: userMsg }]);
    setLoading(true);

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMsg,
          disease: "general inquiry",
          crop: "general",
          is_healthy: true,
          language: langCode,
        }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { from: "ai", text: data.reply }]);
    } catch {
      setMessages(prev => [
        ...prev,
        { from: "ai", text: ERROR_MSG[LANG_CODE_MAP[lang]] || ERROR_MSG.english }
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

  const chips = QUICK_ACTIONS[LANG_CODE_MAP[lang]] || QUICK_ACTIONS.english;

  return (
    <div className="specialist-overlay" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="specialist-modal" role="dialog" aria-modal="true" aria-label="AI Specialist Live Chat">

        {/* ── Header ── */}
        <div className="specialist-header">
          <div className="specialist-header-inner">
            <div className="specialist-avatar">🧑‍🌾</div>
            <div style={{ flex: 1 }}>
              <div className="specialist-name">Dr. Agro AI</div>
              <div className="specialist-role">AI Crop Disease Specialist · PhD Agronomy</div>
              <div className="specialist-status">
                <div className="fab-pulse" />
                Online now
              </div>
            </div>
          </div>
          <button className="specialist-close-btn" onClick={onClose} aria-label="Close chat">✕</button>

          {/* Credential chips */}
          <div className="specialist-info-bar" style={{ marginTop: 14, position: "relative", zIndex: 1 }}>
            <span className="info-chip">🌱 38 Diseases</span>
            <span className="info-chip">🌍 4 Languages</span>
            <span className="info-chip">⚡ Instant Reply</span>
            <span className="info-chip">🆓 Free Forever</span>
          </div>
        </div>

        {/* ── Messages ── */}
        <div className="specialist-body" id="specialist-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`msg-wrap ${msg.from}`}>
              <div className={`msg-bubble ${msg.from}`}>
                {msg.from === "ai" && (
                  <div className="msg-sender">🌿 Dr. Agro AI</div>
                )}
                {msg.text}
              </div>
            </div>
          ))}

          {loading && (
            <div className="msg-wrap ai">
              <div className="msg-bubble ai">
                <div className="msg-sender">🌿 Dr. Agro AI</div>
                <div className="typing-dots">
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* ── Quick Action Chips ── */}
        <div className="specialist-chips">
          {chips.map((chip, i) => (
            <button
              key={i}
              className="specialist-chip"
              onClick={() => send(chip)}
              disabled={loading}
            >
              {chip}
            </button>
          ))}
        </div>

        {/* ── Input ── */}
        <div className="specialist-footer">
          <div className="specialist-input-row">
            <input
              ref={inputRef}
              id="specialist-chat-input"
              className="specialist-input"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder={PLACEHOLDER[LANG_CODE_MAP[lang]] || PLACEHOLDER.english}
              disabled={loading}
            />
            <button
              id="specialist-chat-send"
              className="specialist-send"
              onClick={() => send()}
              disabled={loading || !input.trim()}
            >
              Send ↑
            </button>
          </div>
          <p style={{ fontSize: 10, color: "var(--text-3)", marginTop: 8, textAlign: "center" }}>
            AI responses are informational. Always consult a local agronomist for critical decisions.
          </p>
        </div>
      </div>
    </div>
  );
}
