import { useState } from "react";
import CameraCapture from "./components/CameraCapture";
import ResultCard from "./components/ResultCard";
import Loader from "./components/Loader";

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
      const res = await fetch("http://10.34.158.217:8000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.error) setError(data.error);
      else setResult(data);
    } catch {
      setError("Cannot connect to server. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
    setPreview(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white">
      {/* Header */}
      <header className="bg-green-700 text-white py-4 px-6 shadow-lg">
        <div className="max-w-2xl mx-auto flex items-center gap-3">
          <span className="text-3xl">🌿</span>
          <div>
            <h1 className="text-xl font-bold">Crop Doctor</h1>
            <p className="text-green-200 text-xs">AI-Powered Crop Disease Detection</p>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="max-w-2xl mx-auto px-4 py-8">
        {!result && !loading && (
          <CameraCapture onCapture={diagnose} preview={preview} />
        )}
        {loading && <Loader />}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-5 text-center">
            <p className="text-red-600 font-medium">⚠️ {error}</p>
            <button
              onClick={reset}
              className="mt-4 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
            >
              Try Again
            </button>
          </div>
        )}
        {result && <ResultCard result={result} preview={preview} onReset={reset} />}
      </main>

      {/* Footer */}
      <footer className="text-center py-6 text-gray-400 text-xs">
        Crop Doctor v1.0 — Free for farmers
      </footer>
    </div>
  );
}