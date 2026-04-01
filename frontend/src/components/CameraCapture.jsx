import { useRef, useState } from "react";
import { useTranslation } from '../LanguageContext';

const CROPS = [
  { emoji: "🍅", name: "Tomato" }, { emoji: "🥔", name: "Potato" },
  { emoji: "🌽", name: "Corn" }, { emoji: "🍎", name: "Apple" },
  { emoji: "🍇", name: "Grape" }, { emoji: "🍑", name: "Peach" },
  { emoji: "🌾", name: "Wheat" }, { emoji: "🌿", name: "Rice" },
  { emoji: "🌶️", name: "Pepper" }, { emoji: "🍓", name: "Strawberry" },
  { emoji: "🫐", name: "Blueberry" }, { emoji: "🍊", name: "Orange" },
  { emoji: "🌱", name: "Soybean" }, { emoji: "🍒", name: "Cherry" },
];

export default function CameraCapture({ onCapture, preview }) {
  const t = useTranslation();
  const cameraRef = useRef();
  const galleryRef = useRef();
  const [dragOver, setDragOver] = useState(false);

  const handleFile = (e) => {
    const file = e.target.files[0];
    if (file) onCapture(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) onCapture(file);
  };

  return (
    <div>
      {/* Upload section */}
      <div style={{ padding: "24px 24px 20px" }}>

        {/* Camera button — primary */}
        <div
          onClick={() => cameraRef.current.click()}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          style={{
            border: `2px dashed ${dragOver ? "#2d8a4e" : "#c8e6c9"}`,
            borderRadius: 20,
            padding: "32px 20px",
            textAlign: "center",
            cursor: "pointer",
            background: dragOver ? "#f0faf0" : preview ? "#f8fdf8" : "#f8fdf8",
            transition: "all 0.2s",
            marginBottom: 12,
            position: "relative",
            overflow: "hidden"
          }}
        >
          {preview ? (
            <div>
              <img src={preview} alt="preview" style={{
                maxHeight: 200, maxWidth: "100%", borderRadius: 14,
                objectFit: "contain", margin: "0 auto", display: "block"
              }} />
              <p style={{ color: "#2d8a4e", fontSize: 12, marginTop: 10, fontWeight: 500 }}>
                ✓ {t('upload_hint')}
              </p>
            </div>
          ) : (
            <div>
              <div style={{
                width: 64, height: 64, borderRadius: 18, margin: "0 auto 14px",
                background: "linear-gradient(135deg, #1a5c30, #2d8a4e)",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 28, boxShadow: "0 8px 24px rgba(45,138,78,0.25)"
              }}>📸</div>
              <p style={{ fontFamily: "'Fraunces', serif", fontSize: 18, color: "#1a3a22", margin: "0 0 6px" }}>
                {t('take_photo')}
              </p>
              <p style={{ color: "#999", fontSize: 12, margin: 0 }}>
                {t('upload_hint')}
              </p>
            </div>
          )}
        </div>

        {/* Hidden camera input */}
        <input ref={cameraRef} type="file" accept="image/*"
          capture="environment" onChange={handleFile} style={{ display: "none" }} />

        {/* Gallery upload — secondary */}
        <button
          onClick={() => galleryRef.current.click()}
          style={{
            width: "100%", padding: "13px 16px",
            border: "1.5px solid #e0e0e0", borderRadius: 14,
            background: "#fff", fontSize: 13, color: "#555",
            cursor: "pointer", fontFamily: "'DM Sans', sans-serif",
            display: "flex", alignItems: "center", justifyContent: "center",
            gap: 8, transition: "all 0.15s"
          }}
          onMouseEnter={e => { e.target.style.borderColor = "#2d8a4e"; e.target.style.color = "#2d8a4e"; }}
          onMouseLeave={e => { e.target.style.borderColor = "#e0e0e0"; e.target.style.color = "#555"; }}
        >
          🖼️ {t('upload_photo')}
        </button>

        {/* Hidden gallery input */}
        <input ref={galleryRef} type="file" accept="image/*"
          onChange={handleFile} style={{ display: "none" }} />

        {/* Diagnose button — shows when preview exists */}
        {preview && (
          <button
            onClick={() => {}}
            style={{
              width: "100%", marginTop: 10, padding: "15px",
              background: "linear-gradient(135deg, #1a5c30, #2d8a4e)",
              color: "#fff", border: "none", borderRadius: 14,
              fontSize: 15, fontWeight: 500, cursor: "pointer",
              fontFamily: "'DM Sans', sans-serif",
              boxShadow: "0 6px 20px rgba(45,138,78,0.3)"
            }}
          >
            🔍 {t('diagnose_button')}
          </button>
        )}
      </div>

      {/* Divider */}
      <div style={{ height: 1, background: "#f0f0f0", margin: "0 24px" }} />

      {/* Supported crops */}
      <div style={{ padding: "20px 24px 24px" }}>
        <p style={{
          fontSize: 10, fontWeight: 500, letterSpacing: "0.1em",
          textTransform: "uppercase", color: "#aaa", marginBottom: 12
        }}>
          {t('supported_crops')} — 38 diseases detected
        </p>
        <div style={{
          display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 8
        }}>
          {CROPS.map((crop) => (
            <div key={crop.name} style={{
              background: "#f5faf5", border: "1px solid #e8f5e9",
              borderRadius: 12, padding: "10px 4px", textAlign: "center",
              cursor: "default", transition: "all 0.15s"
            }}
              onMouseEnter={e => { e.currentTarget.style.background = "#e8f5e9"; e.currentTarget.style.transform = "translateY(-2px)"; }}
              onMouseLeave={e => { e.currentTarget.style.background = "#f5faf5"; e.currentTarget.style.transform = "translateY(0)"; }}
            >
              <div style={{ fontSize: 20, marginBottom: 3 }}>{crop.emoji}</div>
              <div style={{ fontSize: 10, color: "#555", fontWeight: 500 }}>{crop.name}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
