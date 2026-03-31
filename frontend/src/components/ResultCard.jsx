import ChatBox from "./ChatBox";
export default function ResultCard({ result, preview, onReset }) {
  const severityColor = {
    None: "bg-green-100 text-green-700",
    Mild: "bg-yellow-100 text-yellow-700",
    Moderate: "bg-orange-100 text-orange-700",
    Severe: "bg-red-100 text-red-700",
    Unknown: "bg-gray-100 text-gray-600",
  };

  return (
    <div className="space-y-4">
      {/* Top result card */}
      <div className={`rounded-2xl p-5 shadow-sm border ${
        result.is_healthy
          ? "bg-green-50 border-green-200"
          : "bg-red-50 border-red-200"
      }`}>
        <div className="flex items-start gap-4">
          {preview && (
            <img
              src={preview}
              alt="leaf"
              className="w-20 h-20 rounded-xl object-cover flex-shrink-0"
            />
          )}
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">{result.is_healthy ? "✅" : "⚠️"}</span>
              <span className="font-bold text-lg text-gray-800">
                {result.crop}
              </span>
            </div>
            <p className={`text-base font-semibold ${
              result.is_healthy ? "text-green-700" : "text-red-700"
            }`}>
              {result.disease}
            </p>
            <div className="flex items-center gap-2 mt-2">
              <span className="text-xs bg-white border border-gray-200 px-2 py-1 rounded-full text-gray-600">
                Confidence: {result.confidence}
              </span>
              <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                severityColor[result.severity] || severityColor.Unknown
              }`}>
                {result.severity === "None" ? "Healthy" : result.severity}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Details */}
      {!result.is_healthy && (
        <>
          <InfoRow icon="🔬" label="Cause" value={result.cause} />
          <InfoRow icon="👁️" label="Symptoms" value={result.symptoms} />
          <InfoRow icon="🌿" label="Organic Treatment" value={result.organic_cure} color="green" />
          <InfoRow icon="💊" label="Chemical Treatment" value={result.chemical_cure} color="blue" />
          <InfoRow icon="🛡️" label="Prevention" value={result.prevention} />
          <InfoRow icon="⏱️" label="Recovery Time" value={result.recovery_time} />
        </>
      )}

      {result.is_healthy && (
        <div className="bg-green-50 rounded-2xl p-5 border border-green-200">
          <p className="text-green-700 font-semibold mb-1">🎉 Great news!</p>
          <p className="text-gray-600 text-sm">{result.prevention}</p>
        </div>
      )}

      {/* Top predictions */}
      <div className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
        <p className="text-xs font-semibold text-gray-500 uppercase mb-3">
          Top Predictions
        </p>
        {result.top_predictions?.map((p, i) => (
          <div key={i} className="flex items-center justify-between py-1">
            <span className="text-sm text-gray-700">{p.disease}</span>
            <span className={`text-xs font-medium ${
              i === 0 ? "text-green-600" : "text-gray-400"
            }`}>
              {p.confidence}
            </span>
          </div>
        ))}
      </div>
      {/* Live Chat */}
<ChatBox
  disease={result.disease}
  crop={result.crop}
  is_healthy={result.is_healthy}
/>

      {/* Reset button */}
      <button
        onClick={onReset}
        className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-xl shadow-md transition-colors"
      >
        📸 Diagnose Another Crop
      </button>
    </div>
  );
}

function InfoRow({ icon, label, value, color }) {
  const bg = color === "green"
    ? "bg-green-50 border-green-100"
    : color === "blue"
    ? "bg-blue-50 border-blue-100"
    : "bg-white border-gray-100";

  return (
    <div className={`rounded-xl p-4 border shadow-sm ${bg}`}>
      <p className="text-xs font-semibold text-gray-500 uppercase mb-1">
        {icon} {label}
      </p>
      <p className="text-sm text-gray-700 leading-relaxed">{value}</p>
    </div>
  );
}