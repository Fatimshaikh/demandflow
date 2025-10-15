import React, { useState } from "react";
import axios from "axios";

export default function UploadForm({ setForecastData, setInsight }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");
    setLoading(true);

    try {
      // Upload CSV
      const formData = new FormData();
      formData.append("file", file);
      const uploadRes = await axios.post("http://127.0.0.1:8000/api/upload-csv/", formData);
      const preview = uploadRes.data.preview;

      // Forecast
      const forecastRes = await axios.post("http://127.0.0.1:8000/api/forecast/", {
        data: preview,
        date_column: Object.keys(preview[0])[0],
        value_column: Object.keys(preview[0])[1],
        periods: 10
      });

      setForecastData(forecastRes.data.forecast);

      // LLM Insight
      const insightRes = await axios.post("http://127.0.0.1:8000/api/insight/", {
        forecast: forecastRes.data.forecast
      });

      setInsight(insightRes.data.insight);
    } catch (error) {
      alert("Error: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl p-6 shadow">
      <h2 className="text-xl font-semibold mb-4">📁 Upload Sales Data (CSV)</h2>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
        className="border p-2 rounded w-full mb-4"
      />
      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Processing..." : "Upload & Forecast"}
      </button>
    </div>
  );
}
