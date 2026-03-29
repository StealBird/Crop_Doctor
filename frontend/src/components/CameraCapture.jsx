import { useRef } from "react";

export default function CameraCapture({ onCapture, preview }) {
  const inputRef = useRef();

  const handleFile = (e) => {
    const file = e.target.files[0];
    if (file) onCapture(file);
  };

  return (
    <div className="text-center">
      {/* Hero */}
      <div className="mb-8">
        <div className="text-6xl mb-4">🌾</div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          Diagnose Your Crop
        </h2>
        <p className="text-gray-500 text-sm max-w-sm mx-auto">
          Take a clear photo of the affected leaf. Our AI will identify the
          disease and suggest treatment instantly.
        </p>
      </div>

      {/* Upload area */}
      <div
        onClick={() => inputRef.current.click()}
        className="border-2 border-dashed border-green-300 rounded-2xl p-10 cursor-pointer hover:bg-green-50 transition-colors mb-6 mx-auto max-w-sm"
      >
        {preview ? (
          <img
            src={preview}
            alt="preview"
            className="max-h-48 mx-auto rounded-xl object-contain"
          />
        ) : (
          <div>
            <div className="text-5xl mb-3">📷</div>
            <p className="text-green-700 font-semibold">Tap to take photo</p>
            <p className="text-gray-400 text-xs mt-1">or upload from gallery</p>
          </div>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleFile}
        className="hidden"
      />

      <button
        onClick={() => inputRef.current.click()}
        className="bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-10 rounded-xl text-lg shadow-md transition-colors"
      >
        📸 Take Photo / Upload
      </button>

      {/* Supported crops */}
      <div className="mt-10 text-left bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
        <p className="text-xs font-semibold text-gray-500 uppercase mb-3">
          Supported Crops (38 diseases)
        </p>
        <div className="flex flex-wrap gap-2">
          {["🍅 Tomato","🥔 Potato","🌽 Corn","🍎 Apple","🍇 Grape","🍑 Peach",
            "🌶️ Pepper","🍓 Strawberry","🫐 Blueberry","🍊 Orange","🌱 Soybean",
            "🍒 Cherry","🌿 Squash","🫘 Raspberry"].map((c) => (
            <span
              key={c}
              className="bg-green-50 text-green-700 text-xs px-3 py-1 rounded-full border border-green-100"
            >
              {c}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
