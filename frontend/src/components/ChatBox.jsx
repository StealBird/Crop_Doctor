import { useState, useRef, useEffect } from "react";
import { useLanguage } from '../LanguageContext';

const API = process.env.REACT_APP_API_URL;

const LANG_META = {
  EN: { label: "English",  code: "english" },
  HI: { label: "हिंदी",    code: "hindi" },
  MR: { label: "मराठी",    code: "marathi" },
  HL: { label: "Hinglish", code: "hinglish" },
};

export default function ChatBox({ disease, crop, is_healthy }) {
  const { lang, t, langCode } = useLanguage();

  const getGreeting = () =>
    is_healthy
      ? t('chat_healthy', { crop })
      : t('chat_disease', { crop, disease });

  const [messages, setMessages] = useState([{ from: "ai", text: getGreeting() }]);
  const [input, setInput]       = useState("");
  const [loading, setLoading]   = useState(false);
  const bottomRef = useRef(null);

  // ── Re-generate greeting when language changes (key feature) ──
  useEffect(() => {
    setMessages([{ from: "ai", text: getGreeting() }]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lang]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const suggestions = is_healthy
    ? [t('sug_maintain'), t('sug_fertilizer'), t('sug_next_season')]
    : [t('sug_buy'), t('sug_organic'), t('sug_days'), t('sug_cost')];

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
          language: langCode,
        }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { from: "ai", text: data.reply }]);
    } catch {
      setMessages(prev => [
        ...prev,
        { from: "ai", text: t('chat_error') }
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
    <div className="chatbox">
      {/* ── Header ── */}
      <div className="chatbox-header">
        <div className="chatbox-online-dot" />
        <div>
          <div className="chatbox-title">🌿 {t('chat_title')}</div>
          <div className="chatbox-subtitle">
            {LANG_META[lang]?.label} · AI assistant · instant replies
          </div>
        </div>
      </div>

      {/* ── Messages ── */}
      <div className="chatbox-messages" id="chatbox-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`msg-wrap ${msg.from}`}>
            <div className={`msg-bubble ${msg.from}`}>
              {msg.from === "ai" && (
                <div className="msg-sender">🌿 Crop Doctor</div>
              )}
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="msg-wrap ai">
            <div className="msg-bubble ai">
              <div className="msg-sender">🌿 Crop Doctor</div>
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

      {/* ── Quick chips ── */}
      <div className="chat-chips">
        {suggestions.map((s, i) => (
          <button key={i} className="chat-chip" onClick={() => setInput(s)}>
            {s}
          </button>
        ))}
      </div>

      {/* ── Input ── */}
      <div className="chat-input-row">
        <input
          id="chatbox-input"
          className="chat-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder={t('chat_placeholder')}
        />
        <button
          id="chatbox-send"
          className="chat-send-btn"
          onClick={send}
          disabled={loading || !input.trim()}
        >
          {t('send_btn')}
        </button>
      </div>
    </div>
  );
}
