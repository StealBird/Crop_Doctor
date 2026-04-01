import { useTranslation } from '../LanguageContext';
 
export default function Loader() {
  const t = useTranslation();
 
  return (
    <div style={{ padding: "56px 24px", textAlign: "center" }}>
      <div style={{ position: "relative", width: 80, height: 80, margin: "0 auto 24px" }}>
        <div style={{
          position: "absolute", inset: 0, borderRadius: "50%",
          border: "3px solid #e8f5e9",
        }} />
        <div style={{
          position: "absolute", inset: 0, borderRadius: "50%",
          border: "3px solid transparent",
          borderTopColor: "#2d8a4e",
          animation: "spin 1s linear infinite"
        }} />
        <div style={{
          position: "absolute", inset: "50%", transform: "translate(-50%,-50%)",
          fontSize: 28
        }}>🌿</div>
      </div>
      <p style={{ fontFamily: "'Fraunces', serif", fontSize: 18, color: "#1a3a22", margin: "0 0 6px" }}>
        {t('loading_line1')}
      </p>
      <p style={{ color: "#aaa", fontSize: 13, margin: 0 }}>
        {t('loading_line2')}
      </p>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}