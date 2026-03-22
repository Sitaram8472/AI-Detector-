import React, { useState } from "react";
import { Video } from "lucide-react";

const VideoDetection = () => {
  const [videoName, setVideoName] = useState("");

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Deepfake Video Analysis</h1>
      <div className="bg-gray-900 text-white p-12 rounded-2xl flex flex-col items-center justify-center border-4 border-gray-800">
        <Video size={60} className="text-blue-500 mb-4" />
        <h2 className="text-xl font-medium">Upload Video Clip</h2>
        <p className="text-gray-400 mb-6 text-center">
          We will analyze facial consistency and frame manipulation.
        </p>

        <input
          type="file"
          id="video-upload"
          className="hidden"
          accept="video/*"
          onChange={(e) => setVideoName(e.target.files[0]?.name)}
        />
        <label
          htmlFor="video-upload"
          className="bg-white text-black px-10 py-3 rounded-full font-bold cursor-pointer hover:bg-gray-200 transition"
        >
          {videoName ? videoName : "Select MP4/MOV"}
        </label>
      </div>
    </div>
  );
};

export default VideoDetection;
