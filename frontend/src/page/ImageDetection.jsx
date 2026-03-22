import React, { useState } from "react";
import { Upload, ShieldCheck } from "lucide-react";

const ImageDetection = () => {
  const [image, setImage] = useState(null);

  const handleImageChange = (e) => {
    setImage(URL.createObjectURL(e.target.files[0]));
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

      <button className="w-full mt-6 bg-green-600 text-white py-3 rounded-xl font-semibold flex items-center justify-center gap-2 hover:bg-green-700">
        <ShieldCheck size={20} /> Scan for AI Patterns
      </button>
    </div>
  );
};

export default ImageDetection;
