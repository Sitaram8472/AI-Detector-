import React, { useState } from "react";

const TextDetection = () => {
  const [text, setText] = useState("");

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
          <button className="bg-blue-600 text-white px-8 py-2 rounded-lg hover:bg-blue-700">
            Analyze Text
          </button>
        </div>
      </div>
    </div>
  );
};

export default TextDetection;
