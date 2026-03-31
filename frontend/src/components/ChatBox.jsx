import { useState, useRef, useEffect } from "react";

const API = process.env.REACT_APP_API_URL;

export default function ChatBox({ disease, crop, is_healthy }) {
  const [messages, setMessages] = useState([
    {
      from: "ai",
      text: is_healthy
        ? `🎉 Bahut achha! Aapka ${crop} bilkul healthy hai! Koi bhi sawal ho toh poochho — main yahan hoon.`
        : `Namaste! Main aapka Crop Doctor hoon. Aapke ${crop} mein ${disease} detect hua hai. Ghabrao mat — hum milke theek karenge. Koi bhi sawaal poochho! 🌿`
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

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
        }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { from: "ai", text: data.reply }]);
    } catch {
      setMessages(prev => [
        ...prev,
        { from: "ai", text: "Thoda problem aa gaya. Phir se try karein?" }
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

  const suggestions = is_healthy
    ? ["Aage kaise dhyan rakhun?", "Koi fertilizer suggest karo", "Next season tips do"]
    : ["Yeh dawai kahan milegi?", "Organic option hai?", "Kitne din mein theek hoga?", "Kharcha kitna aayega?"];

  return (
    <div className="rounded-2xl border border-green-200 bg-white shadow-sm overflow-hidden">

      {/* Header */}
      <div className="bg-green-700 px-4 py-3 flex items-center gap-2">
        <div className="w-2 h-2 bg-green-300 rounded-full animate-pulse"></div>
        <span className="text-white font-semibold text-sm">Crop Doctor — Live Chat</span>
        <span className="text-green-300 text-xs ml-auto">Hindi / English / हिंदी</span>
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
          <button key={i} onClick={() => { setInput(s); }}
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
          placeholder="Kuch bhi poochho... (Ask anything)"
          className="flex-1 text-sm border border-gray-200 rounded-xl px-4 py-2 outline-none focus:border-green-400 focus:ring-1 focus:ring-green-400"
        />
        <button onClick={send} disabled={loading || !input.trim()}
          className="bg-green-600 hover:bg-green-700 disabled:opacity-40 text-white px-4 py-2 rounded-xl text-sm font-medium transition-colors">
          भेजो
        </button>
      </div>
    </div>
  );
}