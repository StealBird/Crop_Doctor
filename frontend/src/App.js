import { useState } from "react";
import CameraCapture from "./components/CameraCapture";
import ResultCard from "./components/ResultCard";
import Loader from "./components/Loader";
import './App.css';

const API = process.env.REACT_APP_API_URL;

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [preview, setPreview] = useState(null);

  const diagnose = async (file) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setPreview(URL.createObjectURL(file));
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch(`${API}/predict`, { method: "POST", body: formData });
      const data = await res.json();
      if (data.detail) setError(data.detail);
      else setResult(data);
    } catch {
      setError("Cannot connect to server. Please try again in a moment.");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => { setResult(null); setError(null); setPreview(null); };

  return (
    <div style={{ minHeight: "100vh", background: "#f0f4f0" }}>
      {/* Header */}
      <header style={{
        background: "linear-gradient(160deg, #0a2e1a 0%, #0f4a24 60%, #1a6b2f 100%)",
        padding: "28px 24px 40px",
        position: "relative",
        overflow: "hidden"
      }}>
        {/* Subtle pattern overlay */}
        <div style={{
          position: "absolute", inset: 0, opacity: 0.04,
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23fff' fill-opacity='1'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40'/%3E%3C/g%3E%3C/svg%3E")`
        }} />

        <div style={{ maxWidth: 520, margin: "0 auto", position: "relative" }}>
          {/* Logo */}
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
            <div style={{
              width: 44, height: 44, background: "rgba(255,255,255,0.12)",
              borderRadius: 14, display: "flex", alignItems: "center",
              justifyContent: "center", fontSize: 22, backdropFilter: "blur(8px)"
            }}>🌿</div>
            <div>
              <div style={{ fontFamily: "'Fraunces', serif", color: "#fff", fontSize: 20, fontWeight: 600 }}>
                Crop Doctor
              </div>
              <div style={{ color: "rgba(255,255,255,0.5)", fontSize: 11, letterSpacing: "0.05em", textTransform: "uppercase" }}>
                AI Disease Detection
              </div>
            </div>
          </div>

          {/* Hero text */}
          <h1 style={{ fontFamily: "'Fraunces', serif", color: "#fff", fontSize: 28, lineHeight: 1.2, margin: "0 0 8px" }}>
            Diagnose your crop.<br />
            <em style={{ color: "#7dd87a", fontStyle: "italic" }}>Instantly.</em>
          </h1>
          <p style={{ color: "rgba(255,255,255,0.55)", fontSize: 13, lineHeight: 1.5, margin: 0 }}>
            38 diseases · 14 crops · Free for every farmer
          </p>
        </div>
      </header>

      {/* Main content */}
      <main style={{ maxWidth: 520, margin: "0 auto", padding: "0 16px 40px", marginTop: -16 }}>
        <div style={{ background: "#fff", borderRadius: 24, overflow: "hidden", boxShadow: "0 4px 24px rgba(0,0,0,0.08)" }}>
          {!result && !loading && (
            <CameraCapture onCapture={diagnose} preview={preview} />
          )}
          {loading && <Loader />}
          {error && (
            <div style={{ padding: 24, textAlign: "center" }}>
              <div style={{ fontSize: 32, marginBottom: 12 }}>⚠️</div>
              <p style={{ color: "#c62828", fontWeight: 500, marginBottom: 16 }}>{error}</p>
              <button onClick={reset} style={{
                background: "#2d8a4e", color: "#fff", border: "none",
                padding: "12px 28px", borderRadius: 12, fontSize: 14,
                fontFamily: "'DM Sans', sans-serif", cursor: "pointer"
              }}>Try Again</button>
            </div>
          )}
          {result && <ResultCard result={result} preview={preview} onReset={reset} />}
        </div>
      </main>

      <footer style={{ textAlign: "center", paddingBottom: 24, color: "#aaa", fontSize: 12 }}>
        Crop Doctor v1.0 — Free for every farmer 🌿
      </footer>
    </div>
  );
}