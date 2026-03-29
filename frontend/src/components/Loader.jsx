export default function Loader() {
  return (
    <div className="text-center py-16">
      <div className="text-5xl mb-4 animate-bounce">🔍</div>
      <h3 className="text-lg font-semibold text-gray-700 mb-2">
        Analysing your crop...
      </h3>
      <p className="text-gray-400 text-sm">AI is examining the leaf</p>
      <div className="mt-6 flex justify-center gap-1">
        {[0,1,2].map(i => (
          <div
            key={i}
            className="w-2 h-2 bg-green-500 rounded-full animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>
    </div>
  );
}