import ChatBox from "./ChatBox";

const SEVERITY_STYLES = {
  None: { bg: "#e8f5e9", color: "#2e7d32", label: "Healthy" },
  Mild: { bg: "#fff8e1", color: "#f57f17", label: "Mild" },
  Moderate: { bg: "#fff3e0", color: "#e65100", label: "Moderate" },
  Severe: { bg: "#fce4ec", color: "#b71c1c", label: "Severe" },
  Unknown: { bg: "#f5f5f5", color: "#616161", label: "Unknown" },
};

const INFO_ROWS = [
  { icon: "🔬", key: "cause", label: "Cause" },
  { icon: "👁️", key: "symptoms", label: "Symptoms" },
  { icon: "🌿", key: "organic_cure", label: "Organic Treatment", highlight: "green" },
  { icon: "💊", key: "chemical_cure", label: "Chemical Treatment", highlight: "blue" },
  { icon: "🛡️", key: "prevention", label: "Prevention" },
  { icon: "⏱️", key: "recovery_time", label: "Recovery Time" },
];

export default function ResultCard({ result, preview, onReset }) {
  const sev = SEVERITY_STYLES[result.severity] || SEVERITY_STYLES.Unknown;
  const headerBg = result.is_healthy
    ? "linear-gradient(135deg, #1b5e20, #2e7d32)"
    : "linear-gradient(135deg, #7f0000, #b71c1c)";

  return (
    <div>
      {/* Disease header */}
      <div style={{ background: headerBg, padding: "20px 20px 24px" }}>
        <div style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
          {preview && (
            <img src={preview} alt="leaf" style={{
              width: 64, height: 64, borderRadius: 14, objectFit: "cover",
              flexShrink: 0, border: "2px solid rgba(255,255,255,0.2)"
            }} />
          )}
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
              <span style={{ fontSize: 18 }}>{result.is_healthy ? "✅" : "⚠️"}</span>
              <span style={{ fontFamily: "'Fraunces', serif", color: "#fff", fontSize: 19, fontWeight: 600 }}>
                {result.crop}
              </span>
            </div>
            <p style={{ color: result.is_healthy ? "#a5d6a7" : "#ef9a9a", fontSize: 14, margin: "0 0 10px", fontWeight: 500 }}>
              {result.disease}
            </p>
            <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
              <span style={{
                background: "rgba(255,255,255,0.15)", color: "#fff",
                fontSize: 11, padding: "3px 10px", borderRadius: 20
              }}>
                {result.confidence} confidence
              </span>
              <span style={{
                background: sev.bg, color: sev.color,
                fontSize: 11, padding: "3px 10px", borderRadius: 20, fontWeight: 500
              }}>
                {sev.label}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Info rows */}
      <div style={{ padding: "0 20px" }}>
        {result.is_healthy ? (
          <div style={{
            background: "#f1f8f1", borderRadius: 16, padding: "16px 18px",
            margin: "16px 0", borderLeft: "4px solid #2d8a4e"
          }}>
            <p style={{ color: "#1b5e20", fontWeight: 500, margin: "0 0 4px" }}>🎉 Great news!</p>
            <p style={{ color: "#444", fontSize: 13, lineHeight: 1.5, margin: 0 }}>{result.prevention}</p>
          </div>
        ) : (
          INFO_ROWS.map(({ icon, key, label, highlight }) => (
            result[key] && result[key] !== "Not required" && (
              <div key={key} style={{
                display: "flex", gap: 12, padding: "13px 0",
                borderBottom: "1px solid #f5f5f5", alignItems: "flex-start"
              }}>
                <span style={{ fontSize: 16, marginTop: 1, flexShrink: 0 }}>{icon}</span>
                <div style={{ flex: 1 }}>
                  <p style={{
                    fontSize: 9, fontWeight: 500, letterSpacing: "0.1em",
                    textTransform: "uppercase", color: "#bbb", margin: "0 0 3px"
                  }}>{label}</p>
                  <p style={{
                    fontSize: 13, color: highlight === "green" ? "#1b5e20" : highlight === "blue" ? "#0d47a1" : "#333",
                    lineHeight: 1.5, margin: 0,
                    background: highlight === "green" ? "#f1f8f1" : highlight === "blue" ? "#e3f2fd" : "transparent",
                    padding: highlight ? "6px 10px" : 0,
                    borderRadius: highlight ? 8 : 0
                  }}>{result[key]}</p>
                </div>
              </div>
            )
          ))
        )}

        {/* Top predictions */}
        {result.top_predictions && (
          <div style={{ padding: "14px 0" }}>
            <p style={{
              fontSize: 9, fontWeight: 500, letterSpacing: "0.1em",
              textTransform: "uppercase", color: "#bbb", marginBottom: 10
            }}>Top predictions</p>
            {result.top_predictions.map((p, i) => (
              <div key={i} style={{
                display: "flex", justifyContent: "space-between",
                alignItems: "center", padding: "5px 0"
              }}>
                <span style={{ fontSize: 12, color: "#666" }}>{p.disease}</span>
                <span style={{
                  fontSize: 12, fontWeight: 500,
                  color: i === 0 ? "#2d8a4e" : "#bbb"
                }}>{p.confidence}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Chat */}
      <div style={{ padding: "8px 20px 20px" }}>
        <ChatBox disease={result.disease} crop={result.crop} is_healthy={result.is_healthy} />
      </div>

      {/* Reset */}
      <div style={{ padding: "0 20px 24px" }}>
        <button onClick={onReset} style={{
          width: "100%", padding: "15px",
          background: "linear-gradient(135deg, #1a5c30, #2d8a4e)",
          color: "#fff", border: "none", borderRadius: 14, fontSize: 14,
          fontWeight: 500, cursor: "pointer", fontFamily: "'DM Sans', sans-serif",
          boxShadow: "0 6px 20px rgba(45,138,78,0.25)"
        }}>
          📸 Diagnose another crop
        </button>
      </div>
    </div>
  );
}