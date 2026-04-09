import React, { useState } from "react";
import { analyzeText } from "../lib/api";

const TextDetection = () => {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzeText(text);
      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to analyze text.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">AI Text Regressor</h1>
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <textarea
          className="w-full h-64 p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none resize-none"
          placeholder="Paste the text you want to analyze here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>

        <div className="flex justify-between items-center mt-4">
          <span className="text-sm text-gray-500">
            {text.split(/\s+/).filter(Boolean).length} Words
          </span>
          <button
            className="bg-blue-600 text-white px-8 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-60"
            onClick={handleAnalyze}
            disabled={loading || !text.trim()}
          >
            {loading ? "Analyzing..." : "Analyze Text"}
          </button>
        </div>
      </div>

      {error ? (
        <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
          {error}
        </div>
      ) : null}

      {result ? (
        <div className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm uppercase tracking-wide text-slate-500">Result</p>
          <h2 className="mt-2 text-2xl font-bold text-slate-900">
            {result.prediction}
          </h2>
          {result.confidence ? (
            <p className="mt-2 text-slate-600">Confidence: {result.confidence}</p>
          ) : null}
          <p className="mt-2 text-slate-600">Likely Source: {result.likely_source}</p>
        </div>
      ) : null}
    </div>
  );
};

export default TextDetection;
