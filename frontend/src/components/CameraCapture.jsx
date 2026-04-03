import { useRef, useState } from "react";
import { useLanguage } from '../LanguageContext';

const CROPS = [
  { emoji: "🍅", name: "Tomato" }, { emoji: "🥔", name: "Potato" },
  { emoji: "🌽", name: "Corn" },   { emoji: "🍎", name: "Apple" },
  { emoji: "🍇", name: "Grape" },  { emoji: "🍑", name: "Peach" },
  { emoji: "🌾", name: "Wheat" },  { emoji: "🌿", name: "Rice" },
  { emoji: "🌶️", name: "Pepper" }, { emoji: "🍓", name: "Strawberry" },
  { emoji: "🫐", name: "Blueberry" },{ emoji: "🍊", name: "Orange" },
  { emoji: "🌱", name: "Soybean" },{ emoji: "🍒", name: "Cherry" },
];

export default function CameraCapture({ onCapture, preview }) {
  const { t } = useLanguage();
  const cameraRef  = useRef();
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
      {/* ── Upload zone ── */}
      <div className="upload-zone">

        {/* Drop area */}
        <div
          id="drop-area"
          className={`drop-area${dragOver ? " drag-over" : ""}`}
          onClick={() => cameraRef.current.click()}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          role="button"
          tabIndex={0}
          aria-label="Take or upload a crop photo"
          onKeyDown={e => e.key === "Enter" && cameraRef.current.click()}
        >
          {preview ? (
            <div>
              <img
                src={preview}
                alt="Crop preview"
                style={{
                  maxHeight: 200, maxWidth: "100%", borderRadius: 14,
                  objectFit: "contain", margin: "0 auto", display: "block",
                  boxShadow: "0 8px 24px rgba(0,0,0,0.1)"
                }}
              />
              <p style={{ color: "var(--primary)", fontSize: 12, marginTop: 12, fontWeight: 600 }}>
                ✓ {t('upload_hint')}
              </p>
            </div>
          ) : (
            <div>
              <div className="upload-icon">📸</div>
              <p className="upload-title">{t('take_photo')}</p>
              <p className="upload-hint">{t('upload_hint')}</p>
            </div>
          )}
        </div>

        {/* Hidden camera input */}
        <input
          ref={cameraRef}
          type="file"
          accept="image/jpeg,image/jpg,image/png,image/webp"
          capture="environment"
          onChange={handleFile}
          style={{ display: "none" }}
          id="camera-input"
        />

        {/* Gallery button */}
        <button
          id="btn-gallery-upload"
          className="gallery-btn"
          onClick={() => galleryRef.current.click()}
        >
          🖼️ {t('upload_photo')}
        </button>

        {/* Hidden gallery input */}
        <input
          ref={galleryRef}
          type="file"
          accept="image/jpeg,image/jpg,image/png,image/webp"
          onChange={handleFile}
          style={{ display: "none" }}
          id="gallery-input"
        />

        {/* Diagnose button */}
        {preview && (
          <button id="btn-diagnose" className="diagnose-btn">
            🔍 {t('diagnose_button')}
          </button>
        )}
      </div>

      {/* ── Divider ── */}
      <div className="divider" />

      {/* ── Supported crops ── */}
      <div className="crops-section">
        <p className="section-label">
          {t('supported_crops')} — 38 diseases detected
        </p>
        <div className="crops-grid">
          {CROPS.map((crop) => (
            <div key={crop.name} className="crop-chip">
              <div className="emoji">{crop.emoji}</div>
              <div className="name">{crop.name}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
