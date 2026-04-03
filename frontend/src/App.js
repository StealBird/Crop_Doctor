import { useState, useEffect } from "react";
import CameraCapture from "./components/CameraCapture";
import Loader from "./components/Loader";
import ResultCard from "./components/ResultCard";
import ChatBox from "./components/ChatBox";
import './App.css';
import { useLanguage, LANG_OPTIONS } from './LanguageContext';

const API = process.env.REACT_APP_API_URL;

export default function App() {
  const { lang, switchLang, t, langCode } = useLanguage();
  const [serverWaking, setServerWaking] = useState(false);
  const [showLangMenu, setShowLangMenu] = useState(false);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [preview, setPreview] = useState(null);
  const [showChat, setShowChat] = useState(false);
  const [imageFile, setImageFile] = useState(null);

  const currentLang = LANG_OPTIONS.find(l => l.code === lang);

  // Wake up Render backend on load
  useEffect(() => {
    const wake = async () => {
      try {
        setServerWaking(true);
        await fetch(`${API}/`);
      } catch {
        // silent
      } finally {
        setServerWaking(false);
      }
    };
    wake();
  }, []);

  // When language changes, if we have an image and a result, re-diagnose to translate
  useEffect(() => {
    if (result && imageFile) {
      // Create a dummy file if needed, but imageFile is exactly what was passed
      diagnose(imageFile);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [langCode]);

  const diagnose = async (file) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setShowChat(false);
    setImageFile(file);
    setPreview(URL.createObjectURL(file));
    const formData = new FormData();
    formData.append("file", file);
    formData.append("language", langCode);
    try {
      const res = await fetch(`${API}/predict`, { method: "POST", body: formData });
      const data = await res.json();
      if (data.detail) {
        setError(data.detail);
      } else if (data.error === 'not_a_crop') {
        setError('not_a_crop');
      } else if (data.error) {
        setError(t('error_try_again'));
      } else {
        setResult(data);
      }
    } catch {
      setError(t('error_api_down'));
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
    setPreview(null);
    setShowChat(false);
    setImageFile(null);
  };

  return (
    <div className="app-shell">

      {/* ── Header ── */}
      <header className="app-header" onClick={() => showLangMenu && setShowLangMenu(false)}>
        <div className="curve-bottom" />
        <div className="header-inner">
          <div className="header-top-row">
            <div className="brand">
              <div className="brand-icon">🌿</div>
              <div>
                <div className="brand-name">{t('app_title')}</div>
                <div className="brand-sub">{t('app_tagline')}</div>
              </div>
            </div>

            {/* ── Language flag dropdown ── */}
            <div style={{ position: 'relative' }}>
              <button
                id="btn-lang-selector"
                onClick={(e) => { e.stopPropagation(); setShowLangMenu(m => !m); }}
                style={{
                  display: 'flex', alignItems: 'center', gap: 6,
                  background: 'rgba(255,255,255,0.12)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  color: '#fff', padding: '8px 12px', borderRadius: 10,
                  cursor: 'pointer', fontSize: 13, fontFamily: "'DM Sans',sans-serif"
                }}
              >
                <span>{currentLang?.flag}</span>
                <span>{currentLang?.label}</span>
                <span style={{ color: 'rgba(255,255,255,0.6)', fontSize: 10 }}>▾</span>
              </button>

              {showLangMenu && (
                <div style={{
                  position: 'absolute', right: 0, top: 44,
                  background: '#fff', borderRadius: 12,
                  boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
                  overflow: 'hidden', zIndex: 200, minWidth: 148,
                  border: '1px solid #e0e0e0'
                }}>
                  {LANG_OPTIONS.map(l => (
                    <button
                      key={l.code}
                      onClick={(e) => { e.stopPropagation(); switchLang(l.code); setShowLangMenu(false); }}
                      style={{
                        width: '100%', display: 'flex', alignItems: 'center', gap: 10,
                        padding: '11px 16px', border: 'none',
                        background: lang === l.code ? '#f0faf0' : '#fff',
                        color: lang === l.code ? '#1b5e20' : '#444',
                        fontWeight: lang === l.code ? 600 : 400,
                        fontSize: 13, cursor: 'pointer',
                        fontFamily: "'DM Sans',sans-serif", textAlign: 'left'
                      }}
                    >
                      <span>{l.flag}</span>
                      <span>{l.label}</span>
                      {lang === l.code && <span style={{ marginLeft: 'auto', color: '#2d8a4e', fontSize: 12 }}>✓</span>}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="header-hero">
            <h1>
              {t('diagnose_title')}<br />
              <em>{t('diagnose_italic')}</em>
            </h1>
            <p>{t('diagnose_sub')}</p>
            <div className="header-stats">
              <span className="header-stat-pill">🌿 {t('stat_crops')}</span>
              <span className="header-stat-pill">{t('stat_diseases')}</span>
              <span className="header-stat-pill alert">🔶 {t('stat_ai')}</span>
            </div>
          </div>

          {serverWaking && (
            <div className="wake-banner">
              <div className="wake-dot" />
              <span className="wake-text">
                Starting server… first diagnosis may take ~30 seconds
              </span>
            </div>
          )}
        </div>
      </header>

      {/* ── Main card — always shows upload, result appears below ── */}
      <main className="main-card" role="main">
        <div className="card">

          {/* ── Upload section — always visible unless loading ── */}
          {!loading && !result && (
            <CameraCapture onCapture={diagnose} preview={preview} />
          )}

          {/* ── Loader ── */}
          {loading && <Loader />}

          {/* ── Errors ── */}
          {error && !loading && (
            error === 'not_a_crop' ? (
              <div className="error-box" style={{ borderColor: '#f97316', background: 'linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)' }}>
                <div className="error-icon">🌿</div>
                <p className="error-msg" style={{ color: '#9a3412' }}>{t('error_not_crop')}</p>
                <button id="btn-try-again" className="diagnose-btn" onClick={reset}
                  style={{ background: 'linear-gradient(135deg, #f97316, #ea580c)' }}>
                  📸 {t('try_again')}
                </button>
              </div>
            ) : (
              <div className="error-box">
                <div className="error-icon">⚠️</div>
                <p className="error-msg">{error}</p>
                <button id="btn-try-again" className="diagnose-btn" onClick={reset}>
                  {t('try_again')}
                </button>
              </div>
            )
          )}

          {/* ── Result card — shown after successful diagnosis ── */}
          {result && !loading && (
            <ResultCard 
              result={result} 
              preview={preview} 
              onReset={reset} 
              onOpenSpecialist={() => {
                setShowChat(true);
                setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
              }} 
            />
          )}

        </div>

        {/* ── ChatBox — shown after successful diagnosis at the bottom ── */}
        {showChat && result && !loading && (
          <div className="card" style={{ marginTop: 16 }}>
            <ChatBox disease={result.disease} crop={result.crop} is_healthy={result.is_healthy} />
          </div>
        )}

      </main>

      {/* ── Footer ── */}
      <footer className="app-footer">
        {t('footer')} 🌿
      </footer>
    </div>
  );
}