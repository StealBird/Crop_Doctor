import { useLanguage } from '../LanguageContext';

const SEVERITY_MAP = {
  None:     { bg: "#dcfce7", color: "#15803d", label: "Healthy",  dot: "#22c55e" },
  Mild:     { bg: "#fef9c3", color: "#854d0e", label: "Mild",     dot: "#eab308" },
  Moderate: { bg: "#ffedd5", color: "#9a3412", label: "Moderate", dot: "#f97316" },
  Severe:   { bg: "#fee2e2", color: "#991b1b", label: "Severe",   dot: "#ef4444" },
  Unknown:  { bg: "#f3f4f6", color: "#374151", label: "Unknown",  dot: "#9ca3af" },
};

function parseConfidence(conf) {
  if (!conf) return 0;
  return parseFloat(String(conf).replace('%', '')) || 0;
}

export default function ResultCard({ result, preview, onReset, onOpenSpecialist }) {
  const { t } = useLanguage();
  const sev = SEVERITY_MAP[result.severity] || SEVERITY_MAP.Unknown;
  const confNum = parseConfidence(result.confidence);

  // Pick meter color based on confidence
  const meterColor =
    confNum >= 85 ? '#22c55e' :
    confNum >= 60 ? '#f97316' : '#ef4444';

  // Width clamped to 100%
  const meterWidth = `${Math.min(Math.max(confNum, 2), 100)}%`;

  const GRID_ITEMS = [
    { icon: "🔬", label: "CAUSE",      value: result.cause      || "—" },
    { icon: "👁",  label: "SYMPTOMS",  value: result.symptoms    || "—" },
    { icon: "🌱", label: "TREATMENT",  value: result.organic_cure || result.chemical_cure || "—" },
    { icon: "🛡",  label: "PREVENTION",value: result.prevention  || "—" },
  ];

  const handleFindKVK = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        ({ coords: { latitude, longitude } }) => {
          window.open(
            `https://www.google.com/maps/search/KVK+Krishi+Vigyan+Kendra/@${latitude},${longitude},12z`,
            '_blank'
          );
        },
        () => window.open('https://www.google.com/maps/search/KVK+Krishi+Vigyan+Kendra+near+me', '_blank')
      );
    } else {
      window.open('https://www.google.com/maps/search/KVK+Krishi+Vigyan+Kendra+near+me', '_blank');
    }
  };

  const handleCallSpecialist = () => window.open('tel:18001801551', '_self');

  return (
    <div className="rc-shell">

      {/* ══ NEW DIAGNOSIS — top of card ══ */}
      <div className="rc-topbar">
        <span className="rc-topbar-label">✅ Diagnosis Complete</span>
        <button id="btn-new-diagnosis" className="rc-topbar-btn" onClick={onReset}>
          📸 New Diagnosis
        </button>
      </div>

      {/* ══ BANNER — orange (diseased) / green (healthy) ══ */}
      <div className={`rc-banner ${result.is_healthy ? 'rc-banner-healthy' : 'rc-banner-diseased'}`}>
        <div className="rc-banner-text">
          <div className="rc-disease-name">
            {result.is_healthy ? '✅' : '⚠️'} {result.crop}
            {result.disease && result.disease !== result.crop && ` – ${result.disease}`}
          </div>
          <div className="rc-confidence-sub">AI Confidence: {result.confidence}</div>
        </div>

        {/* Floating leaf with green glow */}
        {preview && (
          <div className="rc-leaf-wrap">
            <div className="rc-leaf-glow" />
            <img src={preview} alt="Crop leaf" className="rc-leaf-img" />
          </div>
        )}
      </div>

      {/* ══ CONFIDENCE METER ══ */}
      <div className="rc-section rc-meter-section">
        <div className="rc-meter-row">
          <span className="rc-meter-label">AI Confidence Meter</span>
          <span className="rc-meter-value" style={{ color: meterColor }}>
            {result.confidence}
          </span>
        </div>

        {/* Track */}
        <div className="rc-meter-track">
          {/* Filled part */}
          <div
            className="rc-meter-fill"
            style={{ width: meterWidth, backgroundColor: meterColor }}
          />
          {/* Glow dot at end */}
          <div
            className="rc-meter-dot"
            style={{ left: meterWidth, backgroundColor: meterColor,
              boxShadow: `0 0 10px ${meterColor}, 0 0 20px ${meterColor}55` }}
          />
        </div>

        {/* Labels under track */}
        <div className="rc-meter-labels">
          <span>0%</span><span>25%</span><span>50%</span>
          <span>75%</span><span>100%</span>
        </div>

        {/* Severity + recovery pills */}
        <div className="rc-pills-row">
          <span className="rc-pill" style={{ background: sev.bg, color: sev.color }}>
            <span className="rc-pill-dot" style={{ background: sev.dot }} />
            {sev.label}
          </span>
          {result.recovery_time && (
            <span className="rc-pill rc-pill-ghost">⏱ {result.recovery_time}</span>
          )}
          {result.confidence && (
            <span className="rc-pill rc-pill-ghost">
              {confNum >= 85 ? '🎯 High Confidence' : confNum >= 60 ? '⚡ Moderate' : '⚠️ Low Confidence'}
            </span>
          )}
        </div>
      </div>

      {/* ══ AI INTRO MESSAGE ══ */}
      <div className="rc-section">
        <div className="rc-ai-message">
          <div className="rc-ai-avatar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <rect x="3" y="11" width="18" height="11" rx="2"/>
              <path d="M7 11V7a5 5 0 0110 0v4"/>
              <circle cx="12" cy="16" r="1" fill="currentColor"/>
            </svg>
          </div>
          <p className="rc-ai-text">
            {result.ai_summary || (result.is_healthy
              ? `Your ${result.crop} looks completely healthy! No disease detected. Keep up the great care.`
              : `Hello! I've detected ${result.disease} in your ${result.crop}. Don't worry — it's treatable. Ask the AI Specialist anything about treatment, cost, or prevention.`
            )}
          </p>
        </div>
      </div>

      {/* ══ 4-COLUMN INFO GRID (diseased) ══ */}
      {!result.is_healthy && (
        <div className="rc-section">
          <div className="rc-info-grid">
            {GRID_ITEMS.map(({ icon, label, value }) => (
              <div key={label} className="rc-info-card">
                <div className="rc-info-icon">{icon}</div>
                <div className="rc-info-label">{label}</div>
                <div className="rc-info-value">{value}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ══ HEALTHY — prevention block ══ */}
      {result.is_healthy && result.prevention && (
        <div className="rc-section">
          <div className="rc-prevention-healthy">
            <span className="rc-info-icon">🛡</span>
            <div>
              <div className="rc-info-label">PREVENTION TIPS TO STAY HEALTHY</div>
              <div className="rc-info-value" style={{ marginTop: 5 }}>{result.prevention}</div>
            </div>
          </div>
        </div>
      )}

      {/* ══ TOP PREDICTIONS ══ */}
      {result.top_predictions && result.top_predictions.length > 1 && (
        <div className="rc-section">
          <div className="rc-section-label">{t('top_predictions')}</div>
          <div className="rc-preds">
            {result.top_predictions.slice(0, 3).map((p, i) => {
              const pct = parseConfidence(p.confidence);
              return (
                <div key={i} className="rc-pred-row">
                  <span className="rc-pred-name">{p.disease}</span>
                  <div className="rc-pred-bar-wrap">
                    <div
                      className="rc-pred-bar"
                      style={{
                        width: `${pct}%`,
                        backgroundColor: i === 0 ? 'var(--green-600)' : 'var(--border2)',
                      }}
                    />
                  </div>
                  <span className="rc-pred-conf"
                    style={{ color: i === 0 ? 'var(--green-600)' : 'var(--text-3)' }}>
                    {p.confidence}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ══ ACTION BUTTONS — KVK + Call ══ */}
      <div className="rc-section">
        <div className="rc-action-row">
          <button id="btn-find-kvk" className="rc-action-btn" onClick={handleFindKVK}>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
            Find KVK Office
          </button>
          <button id="btn-call-specialist" className="rc-action-btn rc-action-btn-call"
            onClick={handleCallSpecialist}>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.6a19.79 19.79 0 01-3.07-8.68A2 2 0 012 .82h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 8.91A16 16 0 0015.09 17.9l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
            </svg>
            Call Specialist
          </button>
        </div>
      </div>

      {/* ══ CHAT WITH AI DOCTOR — full-width button ══ */}
      <div className="rc-section">
        <button
          id="btn-open-ai-chat"
          className="rc-chat-open-btn"
          onClick={onOpenSpecialist}
        >
          <div className="rc-chat-btn-left">
            <div className="rc-chat-btn-avatar">🧑‍🌾</div>
            <div>
              <div className="rc-chat-btn-title">Chat with AI Specialist</div>
              <div className="rc-chat-btn-sub">
                Ask about {result.is_healthy ? 'fertilizer & growing tips' : `treating ${result.disease}`}
              </div>
            </div>
          </div>
          <div className="rc-chat-btn-arrow">
            <div className="rc-chat-btn-live">
              <span className="rc-chat-live-dot" />
              Live
            </div>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <path d="M9 18l6-6-6-6"/>
            </svg>
          </div>
        </button>
      </div>

      {/* ══ NEW DIAGNOSIS — bottom full width ══ */}
      <div className="rc-section" style={{ paddingTop: 0 }}>
        <button id="btn-new-diagnosis-bottom" className="reset-btn" onClick={onReset}>
          ← {t('back_button')}
        </button>
      </div>

    </div>
  );
}