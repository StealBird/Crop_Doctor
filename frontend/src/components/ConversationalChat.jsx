import { useState, useRef, useEffect, useCallback } from 'react';
import { useLanguage } from '../LanguageContext';

const API = process.env.REACT_APP_API_URL;

const SPEECH_LANG = {
  english: 'en-IN',
  hindi:   'hi-IN',
  marathi: 'mr-IN',
  hinglish:'hi-IN',
};

const SEV_STYLE = {
  None:     { color: '#15803d', bg: '#dcfce7', icon: '✅' },
  Mild:     { color: '#854d0e', bg: '#fef9c3', icon: '⚡' },
  Moderate: { color: '#9a3412', bg: '#ffedd5', icon: '⚠️' },
  Severe:   { color: '#991b1b', bg: '#fee2e2', icon: '🔴' },
  Unknown:  { color: '#374151', bg: '#f3f4f6', icon: '❓' },
};

// ── Thinking bubble ──────────────────────────────────────────────────────────
function ThinkingBubble({ text }) {
  return (
    <div className="cv-row cv-row-ai">
      <div className="cv-avatar">🌿</div>
      <div className="cv-bubble cv-bubble-ai cv-bubble-thinking">
        <span className="cv-think-text">{text}</span>
        <span className="cv-dots"><span /><span /><span /></span>
      </div>
    </div>
  );
}

// ── TTS button ───────────────────────────────────────────────────────────────
function TtsBtn({ text, id, speakingId, onSpeak }) {
  const active = speakingId === id;
  return (
    <button
      className={`cv-tts${active ? ' cv-tts-on' : ''}`}
      onClick={() => onSpeak(text, id)}
      title="Read aloud"
      aria-label="Read aloud"
    >
      {active ? '🔇' : '🔊'}
    </button>
  );
}

// ── Diagnosis card bubble ────────────────────────────────────────────────────
function DiagnosisBubble({ msg, speakingId, onSpeak, onSuggest, t }) {
  const { result } = msg;
  const [open, setOpen] = useState(false);
  const sev = SEV_STYLE[result.severity] || SEV_STYLE.Unknown;
  const ttsText = result.ai_summary || (result.is_healthy
    ? `${result.crop} is healthy.`
    : `${result.disease} detected in ${result.crop} with ${result.confidence} confidence.`);

  const chips = result.is_healthy
    ? [t('sug_maintain'), t('sug_fertilizer'), t('sug_next_season')]
    : [t('sug_buy'), t('sug_organic'), t('sug_days'), t('sug_cost')];

  return (
    <div className="cv-row cv-row-ai">
      <div className="cv-avatar">🌿</div>
      <div className="cv-diag-card">

        {/* Banner */}
        <div className={`cv-diag-banner ${result.is_healthy ? 'cv-banner-green' : 'cv-banner-orange'}`}>
          <div className="cv-diag-crop">{result.is_healthy ? '✅' : '⚠️'} {result.crop}</div>
          {!result.is_healthy && <div className="cv-diag-disease">{result.disease}</div>}
        </div>

        {/* Body */}
        <div className="cv-diag-body">
          <p className="cv-diag-summary">{ttsText}</p>

          <div className="cv-badge-row">
            <span className="cv-badge" style={{ background: sev.bg, color: sev.color }}>
              {sev.icon} {result.severity}
            </span>
            <span className="cv-badge cv-badge-conf">🎯 {result.confidence}</span>
            {result.recovery_time && result.recovery_time !== 'Not applicable' && (
              <span className="cv-badge cv-badge-time">⏱ {result.recovery_time}</span>
            )}
          </div>

          {!result.is_healthy && (
            <button className="cv-expand-btn" onClick={() => setOpen(o => !o)}>
              {open ? t('conv_hide_details') : t('conv_show_details')}
            </button>
          )}

          {open && !result.is_healthy && (
            <div className="cv-detail-list">
              {result.organic_cure && result.organic_cure !== 'Not required' && (
                <div className="cv-detail-item">
                  <span className="cv-detail-icon">🌱</span>
                  <div>
                    <div className="cv-detail-label">Organic</div>
                    <div className="cv-detail-val">{result.organic_cure}</div>
                  </div>
                </div>
              )}
              {result.chemical_cure && result.chemical_cure !== 'Not required' && (
                <div className="cv-detail-item">
                  <span className="cv-detail-icon">💊</span>
                  <div>
                    <div className="cv-detail-label">Chemical</div>
                    <div className="cv-detail-val">{result.chemical_cure}</div>
                  </div>
                </div>
              )}
              {result.prevention && result.prevention !== 'Not required' && (
                <div className="cv-detail-item">
                  <span className="cv-detail-icon">🛡️</span>
                  <div>
                    <div className="cv-detail-label">Prevention</div>
                    <div className="cv-detail-val">{result.prevention}</div>
                  </div>
                </div>
              )}
            </div>
          )}

          <TtsBtn text={ttsText} id={msg.id} speakingId={speakingId} onSpeak={onSpeak} />
        </div>

        {/* Quick-reply chips */}
        <div className="cv-chips">
          {chips.map(c => (
            <button key={c} className="cv-chip" onClick={() => onSuggest(c)}>{c}</button>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Generic message bubble ───────────────────────────────────────────────────
function Bubble({ msg, speakingId, onSpeak, onSuggest, t }) {
  if (msg.type === 'thinking')   return <ThinkingBubble text={msg.content} />;
  if (msg.type === 'diagnosis')  return <DiagnosisBubble msg={msg} speakingId={speakingId} onSpeak={onSpeak} onSuggest={onSuggest} t={t} />;

  const isUser  = msg.role === 'user';
  const isError = msg.type === 'error';
  const isImg   = msg.type === 'image';

  if (isImg) return (
    <div className="cv-row cv-row-user">
      <div className="cv-bubble cv-bubble-user cv-bubble-img">
        <img src={msg.imageUrl} alt="Uploaded crop" className="cv-preview-img" />
        <p className="cv-img-cap">📸 {t('conv_analyzing')}</p>
      </div>
    </div>
  );

  return (
    <div className={`cv-row ${isUser ? 'cv-row-user' : 'cv-row-ai'}`}>
      {!isUser && <div className="cv-avatar">🌿</div>}
      <div className={`cv-bubble ${isUser ? 'cv-bubble-user' : 'cv-bubble-ai'} ${isError ? 'cv-bubble-error' : ''}`}>
        <p>{msg.content}</p>
        {!isUser && !isError && (
          <TtsBtn text={msg.content} id={msg.id} speakingId={speakingId} onSpeak={onSpeak} />
        )}
      </div>
    </div>
  );
}

// ── Preferred Google voice names by language ────────────────────────────────
const PREF_VOICES = {
  hindi:   ['Google हिन्‍दी', 'Google Hindi'],
  marathi: ['Google मराठी', 'Google Marathi'],
  hinglish:['Google हिन्‍दी', 'Google Hindi'],
  english: ['Google UK English Female', 'Google India English Female', 'Google US English'],
};

function getBestVoice(lc) {
  if (!window.speechSynthesis) return null;
  const voices = window.speechSynthesis.getVoices();
  if (!voices.length) return null;
  const targetLang = SPEECH_LANG[lc] || 'en-IN';
  // 1. Exact preferred name
  for (const name of (PREF_VOICES[lc] || [])) {
    const v = voices.find(v => v.name === name);
    if (v) return v;
  }
  // 2. Any Google voice matching two-letter lang code
  const g = voices.find(v => v.lang.startsWith(targetLang.split('-')[0]) && v.name.includes('Google'));
  if (g) return g;
  // 3. Any voice matching full lang code
  return voices.find(v => v.lang === targetLang) || null;
}

// ── Main component ───────────────────────────────────────────────────────────
export default function ConversationalChat({ initialResult = null, initialPreview = null, onReset = null }) {
  const { t, langCode } = useLanguage();
  const [messages,    setMessages]    = useState([]);
  const [inputText,   setInputText]   = useState('');
  const [isListening, setIsListening] = useState(false);
  const [speakingId,  setSpeakingId]  = useState(null);
  const [diagResult,  setDiagResult]  = useState(null);

  const bottomRef  = useRef(null);
  const fileRef    = useRef(null);
  const recRef     = useRef(null);

  const uid = () => `${Date.now()}-${Math.random().toString(36).slice(2)}`;

  // Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Seed messages: show diagnosis immediately if initialResult is given,
  // otherwise show a welcome text. Re-runs when language switches.
  useEffect(() => {
    window.speechSynthesis?.cancel();
    setSpeakingId(null);
    if (initialResult) {
      setDiagResult(initialResult);
      setMessages([{ id: uid(), role: 'ai', type: 'diagnosis', result: initialResult }]);
    } else {
      setMessages([{ id: uid(), role: 'ai', type: 'text', content: t('conv_welcome') }]);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [langCode]);

  const push = useCallback((msg) =>
    setMessages(prev => [...prev, { id: uid(), ...msg }]), []);

  const pushThinking = useCallback((text) => {
    const id = uid();
    setMessages(prev => [...prev, { id, role: 'ai', type: 'thinking', content: text }]);
    return id;
  }, []);

  const removeId = useCallback((id) =>
    setMessages(prev => prev.filter(m => m.id !== id)), []);

  // ── Diagnose image ──────────────────────────────────────────────
  const handleFile = async (file) => {
    if (!file) return;
    const url = URL.createObjectURL(file);
    push({ role: 'user', type: 'image', imageUrl: url, content: file.name });
    const tid = pushThinking(t('conv_thinking_crop'));
    const form = new FormData();
    form.append('file', file);
    form.append('language', langCode);
    try {
      const res  = await fetch(`${API}/predict`, { method: 'POST', body: form });
      const data = await res.json();
      removeId(tid);
      if (data.error === 'not_a_crop') {
        push({ role: 'ai', type: 'error', content: t('error_not_crop') });
      } else if (data.error) {
        push({ role: 'ai', type: 'error', content: t('error_try_again') });
      } else {
        setDiagResult(data);
        push({ role: 'ai', type: 'diagnosis', result: data });
      }
    } catch {
      removeId(tid);
      push({ role: 'ai', type: 'error', content: t('error_api_down') });
    }
  };

  // ── Chat message ────────────────────────────────────────────────
  const sendText = useCallback(async (text) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    push({ role: 'user', type: 'text', content: trimmed });
    setInputText('');
    const tid = pushThinking(t('conv_thinking_chat'));
    try {
      const res  = await fetch(`${API}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message:    trimmed,
          disease:    diagResult?.disease    || 'Unknown',
          crop:       diagResult?.crop       || 'Unknown',
          is_healthy: diagResult?.is_healthy || false,
          language:   langCode,
        }),
      });
      const data = await res.json();
      removeId(tid);
      push({ role: 'ai', type: 'text', content: data.reply });
    } catch {
      removeId(tid);
      push({ role: 'ai', type: 'error', content: t('chat_error') });
    }
  }, [diagResult, langCode, push, pushThinking, removeId, t]);

  // ── TTS with proper language + Google voice preference ────────────
  const speak = useCallback((text, id) => {
    window.speechSynthesis.cancel();
    if (speakingId === id) { setSpeakingId(null); return; }
    const utt   = new SpeechSynthesisUtterance(text);
    utt.lang    = SPEECH_LANG[langCode] || 'en-IN';
    utt.rate    = 0.9;
    utt.pitch   = 1.1;
    const voice = getBestVoice(langCode);
    if (voice) utt.voice = voice;
    utt.onend   = () => setSpeakingId(null);
    utt.onerror = () => setSpeakingId(null);
    window.speechSynthesis.speak(utt);
    setSpeakingId(id);
  }, [speakingId, langCode]);

  // ── Voice input ─────────────────────────────────────────────────
  const toggleMic = useCallback(() => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      push({ role: 'ai', type: 'error', content: 'Voice input not supported in this browser.' });
      return;
    }
    if (isListening) { recRef.current?.stop(); return; }
    const rec     = new SR();
    recRef.current = rec;
    rec.lang      = SPEECH_LANG[langCode] || 'en-IN';
    rec.continuous       = false;
    rec.interimResults   = false;
    rec.onresult  = (e) => { setInputText(e.results[0][0].transcript); setIsListening(false); };
    rec.onerror   = () => setIsListening(false);
    rec.onend     = () => setIsListening(false);
    rec.start();
    setIsListening(true);
  }, [isListening, langCode, push]);

  return (
    <div className="cv-shell">

      {/* Back button — shown only after a diagnosis */}
      {onReset && (
        <div className="cv-topbar">
          <button id="btn-new-diagnosis" className="cv-back-btn" onClick={onReset}>
            ← {t('back_button')}
          </button>
        </div>
      )}

      {/* Message list */}
      <div className="cv-messages">
        {messages.map(msg => (
          <Bubble
            key={msg.id}
            msg={msg}
            speakingId={speakingId}
            onSpeak={speak}
            onSuggest={sendText}
            t={t}
          />
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div className="cv-input-bar">
        <button
          id="btn-conv-upload"
          className="cv-icon-btn"
          onClick={() => fileRef.current?.click()}
          title="Upload crop photo"
          aria-label="Upload photo"
        >📸</button>

        <input
          ref={fileRef}
          type="file"
          accept="image/jpeg,image/jpg,image/png,image/webp"
          style={{ display: 'none' }}
          id="conv-file-input"
          onChange={e => { if (e.target.files[0]) handleFile(e.target.files[0]); e.target.value=''; }}
        />

        <input
          id="conv-text-input"
          className="cv-text-input"
          type="text"
          value={inputText}
          onChange={e => setInputText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendText(inputText)}
          placeholder={t('chat_placeholder')}
          aria-label="Type a message"
        />

        <button
          id="btn-conv-mic"
          className={`cv-icon-btn cv-mic${isListening ? ' cv-mic-on' : ''}`}
          onClick={toggleMic}
          title={isListening ? 'Stop' : 'Voice input'}
          aria-label="Voice input"
        >🎤</button>

        <button
          id="btn-conv-send"
          className="cv-send-btn"
          onClick={() => sendText(inputText)}
          aria-label="Send"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
    </div>
  );
}
