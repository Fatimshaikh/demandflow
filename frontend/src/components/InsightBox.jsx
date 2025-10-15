export default function InsightBox({ text }) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow">
      <h2 className="text-xl font-semibold mb-4">🧠 AI Insight</h2>
      <p className="text-gray-700 whitespace-pre-line">{text}</p>
    </div>
  );
}
