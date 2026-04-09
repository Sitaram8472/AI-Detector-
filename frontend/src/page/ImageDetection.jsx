import React, { useEffect, useState } from "react";
import { Upload, ShieldCheck } from "lucide-react";
import { analyzeImage } from "../lib/api";

const ImageDetection = () => {
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    return () => {
      if (image) {
        URL.revokeObjectURL(image);
      }
    };
  }, [image]);

  const handleImageChange = (e) => {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    if (image) {
      URL.revokeObjectURL(image);
    }

    setFile(selectedFile);
    setResult(null);
    setError("");
    setImage(URL.createObjectURL(selectedFile));
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please upload an image first.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await analyzeImage(file);
      const fakeProbability = Number(data.fake_probability || 0);

      setResult({
        ...data,
        label: fakeProbability >= 0.5 ? "Fake" : "Real",
        confidence: `${Math.round(fakeProbability * 100)}%`,
      });
    } catch (err) {
      setError(err.message || "Failed to analyze image.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">AI Image Detector</h1>
      <div className="bg-white p-8 rounded-2xl border-2 border-dashed border-gray-200 flex flex-col items-center">
        {image ? (
          <img src={image} alt="Preview" className="max-h-64 rounded-lg mb-4" />
        ) : (
          <Upload size={48} className="text-gray-300 mb-4" />
        )}

        <label className="bg-blue-600 text-white px-6 py-2 rounded-lg cursor-pointer hover:bg-blue-700 transition">
          {image ? "Change Image" : "Upload Image"}
          <input
            type="file"
            className="hidden"
            onChange={handleImageChange}
            accept="image/*"
          />
        </label>
        <p className="text-gray-400 text-sm mt-4">
          Supports PNG, JPG up to 10MB
        </p>
      </div>

      <button
        className="w-full mt-6 bg-green-600 text-white py-3 rounded-xl font-semibold flex items-center justify-center gap-2 hover:bg-green-700 disabled:opacity-60"
        onClick={handleAnalyze}
        disabled={loading || !file}
      >
        <ShieldCheck size={20} /> {loading ? "Scanning..." : "Scan for AI Patterns"}
      </button>

      {error ? (
        <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
          {error}
        </div>
      ) : null}

      {result ? (
        <div className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm uppercase tracking-wide text-slate-500">Result</p>
          <h2 className="mt-2 text-2xl font-bold text-slate-900">{result.label}</h2>
          <p className="mt-2 text-slate-600">Fake probability: {result.confidence}</p>
        </div>
      ) : null}
    </div>
  );
};

export default ImageDetection;
