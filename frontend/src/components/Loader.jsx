import { useLanguage } from '../LanguageContext';

export default function Loader() {
  const { t } = useLanguage();

  return (
    <div className="loader-wrap">
      <div className="loader-ring">
        <div className="loader-ring-bg" />
        <div className="loader-ring-spin" />
        <div className="loader-emoji">🌿</div>
      </div>
      <p style={{ fontFamily: "'Fraunces', serif", fontSize: 18, color: "var(--text)", margin: "0 0 6px" }}>
        {t('loading_line1')}
      </p>
      <p style={{ color: "var(--text-3)", fontSize: 13, margin: 0 }}>
        {t('loading_line2')}
      </p>
      <style>{`
        @keyframes spin    { to { transform: rotate(360deg); } }
        @keyframes spinSlow{ to { transform: rotate(-360deg); } }
      `}</style>
    </div>
  );
}