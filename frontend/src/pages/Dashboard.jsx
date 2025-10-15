import React, { useState } from "react";
import UploadForm from "../components/UploadForm";
import ForecastChart from "../components/ForecastChart";
import InsightBox from "../components/InsightBox";

export default function Dashboard() {
  const [forecastData, setForecastData] = useState([]);
  const [insight, setInsight] = useState("");

  return (
    <div className="grid gap-6 max-w-5xl mx-auto">
      <UploadForm setForecastData={setForecastData} setInsight={setInsight} />
      {forecastData.length > 0 && <ForecastChart data={forecastData} />}
      {insight && <InsightBox text={insight} />}
    </div>
  );
}
