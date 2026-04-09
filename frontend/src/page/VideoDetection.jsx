import React, { useEffect, useState } from "react";
import { Video } from "lucide-react";
import { analyzeVideo, getVideoResult } from "../lib/api";

const POLL_INTERVAL_MS = 2500;
const POLL_TIMEOUT_MS = 120000;

const VideoDetection = () => {
  const [videoName, setVideoName] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [taskId, setTaskId] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [polling, setPolling] = useState(false);

  const getProviderLabel = (modelUsed) => {
    if (modelUsed === "truthscan_api") {
      return "TruthScan API";
    }

    return "Local image-model pipeline";
  };

  const getConfidenceLabel = (value) => {
    const numberValue = Number(value ?? 0);
    return `${numberValue.toFixed(2)}%`;
  };

  useEffect(() => {
    if (!taskId || !polling) {
      return undefined;
    }

    const startedAt = Date.now();

    const timer = setInterval(async () => {
      if (Date.now() - startedAt > POLL_TIMEOUT_MS) {
        setError(
          "Video analysis timed out. Celery worker or Redis may be down. Restart both services and try again."
        );
        setPolling(false);
        setResult((prev) => ({
          ...(prev || {}),
          status: "failed",
          message: "Analysis timed out",
        }));
        return;
      }

      try {
        const data = await getVideoResult(taskId);

        if (data.status === "completed") {
          setResult(data);
          setPolling(false);
          return;
        }

        if (data.status === "failed") {
          setError(data.error || "Video analysis failed.");
          setPolling(false);
          return;
        }

        setResult(data);
      } catch (err) {
        setError(err.message || "Failed to fetch video analysis status.");
        setPolling(false);
      }
    }, POLL_INTERVAL_MS);

    return () => clearInterval(timer);
  }, [taskId, polling]);

  const handleVideoChange = (e) => {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);
    setVideoName(selectedFile.name);
    setResult(null);
    setTaskId("");
    setPolling(false);
    setError("");
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please upload a video first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzeVideo(file);

      if (data.status === "failed") {
        setError(data.error || "Unable to start video analysis.");
        return;
      }

      if (data.status === "completed") {
        setResult(data);
        setTaskId("");
        setPolling(false);
        return;
      }

      setTaskId(data.task_id || "");
      setPolling(Boolean(data.task_id));
      setResult({
        status: "processing",
        task_id: data.task_id,
        message: data.message || "Processing started",
      });
    } catch (err) {
      setError(err.message || "Failed to upload video.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-2">Deepfake Video Analysis</h1>
      <p className="text-gray-500 mb-6">
        Detect whether a video is AI-generated using TruthScan API.
      </p>
      <div className="bg-gray-900 text-white p-12 rounded-2xl flex flex-col items-center justify-center border-4 border-gray-800">
        <Video size={60} className="text-blue-500 mb-4" />
        <h2 className="text-xl font-medium">Upload Video Clip</h2>
        <p className="text-gray-400 mb-6 text-center">
          Upload MP4 or MOV and get a fake or real verdict with confidence.
        </p>

        <input
          type="file"
          id="video-upload"
          className="hidden"
          accept="video/*"
          onChange={handleVideoChange}
        />
        <label
          htmlFor="video-upload"
          className="bg-white text-black px-10 py-3 rounded-full font-bold cursor-pointer hover:bg-gray-200 transition"
        >
          {videoName ? videoName : "Select MP4/MOV"}
        </label>
      </div>

      <button
        className="w-full mt-6 bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 disabled:opacity-60"
        onClick={handleAnalyze}
        disabled={loading || !file}
      >
        {loading ? "Analyzing with TruthScan..." : "Start TruthScan Analysis"}
      </button>

      {error ? (
        <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
          {error}
        </div>
      ) : null}

      {result ? (
        <div className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm uppercase tracking-wide text-slate-500">Result</p>

          {result.status === "completed" ? (
            <>
              <h2 className="mt-2 text-2xl font-bold text-slate-900">
                Verdict: {result.verdict}
              </h2>
              <p className="mt-2 text-slate-600">
                Confidence (fake probability): {getConfidenceLabel(result.confidence_percentage)}
              </p>
              <p className="mt-1 text-slate-600">Provider: {getProviderLabel(result.model_used)}</p>
              {typeof result.frames_analyzed === "number" ? (
                <p className="mt-1 text-slate-600">Frames analyzed: {result.frames_analyzed}</p>
              ) : null}
              {result.frame_stride ? (
                <p className="mt-1 text-slate-600">Frame stride: every {result.frame_stride}th frame</p>
              ) : null}
              {result.max_frames_limit ? (
                <p className="mt-1 text-slate-600">Max frames limit: {result.max_frames_limit}</p>
              ) : null}
              {result.error ? (
                <p className="mt-1 text-amber-600">Note: {result.error}</p>
              ) : null}
            </>
          ) : (
            <>
              <h2 className="mt-2 text-2xl font-bold text-slate-900">
                {polling ? "Analyzing video..." : result.message || "Processing started"}
              </h2>
              {polling ? (
                <p className="mt-1 text-slate-600">
                  TruthScan mode is usually faster. This fallback can take up to {Math.round(POLL_TIMEOUT_MS / 1000)} seconds.
                </p>
              ) : null}
              {result.task_id ? (
                <p className="mt-2 text-slate-600">Task ID: {result.task_id}</p>
              ) : null}
            </>
          )}
        </div>
      ) : null}
    </div>
  );
};

export default VideoDetection;
