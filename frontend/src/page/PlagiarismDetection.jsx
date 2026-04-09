import React, { useState } from "react";
import { analyzePlagiarism } from "../lib/api";

const PlagiarismDetection = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);
    setResult(null);
    setError("");
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please upload a text file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzePlagiarism(file);
      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to analyze file.");
    } finally {
      setLoading(false);
    }
  };

  const formatPercent = (value) => `${Number(value || 0).toFixed(2)}%`;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Plagiarism Detection</h1>
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload text document
        </label>

        <input
          type="file"
          accept=".txt,text/plain"
          onChange={handleFileChange}
          className="w-full border border-gray-200 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 outline-none"
        />

        <div className="flex justify-between items-center mt-4">
          <span className="text-sm text-gray-500">
            {file ? file.name : "No file selected"}
          </span>
          <button
            className="bg-blue-600 text-white px-8 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-60"
            onClick={handleAnalyze}
            disabled={loading || !file}
          >
            {loading ? "Analyzing..." : "Check Plagiarism"}
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

          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-semibold text-slate-500">
                Plagiarism Detection
              </p>
              <h2 className="mt-2 text-2xl font-bold text-slate-900">
                {result.plagiarism_label || result.plagiarism}
              </h2>
              <p className="mt-2 text-slate-600">
                {result.plagiarism_explanation || "No explanation available."}
              </p>
              <p className="mt-2 text-slate-500">
                Source: {result.source || "No source found"}
              </p>
              <p className="mt-2 text-slate-500">
                Confidence: {formatPercent(result.confidence?.plagiarism)}
              </p>
            </div>

            <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-semibold text-slate-500">
                AI-Generated Detection
              </p>
              <h2 className="mt-2 text-2xl font-bold text-slate-900">
                {result.ai_generated_label || "AI Detection"}
              </h2>
              <p className="mt-2 text-slate-600">
                {result.ai_explanation || "No explanation available."}
              </p>
              <p className="mt-2 text-slate-500">
                AI Generated: {formatPercent(result.ai_generated_percentage)}
              </p>
              <p className="mt-1 text-slate-500">
                Human Written: {formatPercent(result.human_written_percentage)}
              </p>
              <p className="mt-2 text-slate-500">
                Confidence: {formatPercent(result.confidence?.ai_generated)}
              </p>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default PlagiarismDetection;
