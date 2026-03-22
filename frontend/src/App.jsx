// import React, { useEffect, useState } from "react";

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './page/Dashboard';
import ImageDetection from './page/ImageDetection';
import VideoDetection from './page/VideoDetection';
import TextDetection from './page/TextDetection';
import History from './page/History';

function App() {


  // backend test
  // const [message, setMessage] = useState("");
  // useEffect(() => {
  //   fetch("http://localhost:5000/api/data")
  //     .then((res) => res.json())
  //     .then((data) => setMessage(data.message));
  // }, []);
  // return (
  //   <div>
  //     <h1>My React App</h1>
  //     <h2>{message}</h2>
  //   </div>
  // );


  return (
    <Router>
      <div className="flex min-h-screen bg-gray-50">
        {/* Sidebar will go here later */}
        <div className="flex-1 p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/detect-image" element={<ImageDetection />} />
            <Route path="/detect-video" element={<VideoDetection />} />
            <Route path="/detect-text" element={<TextDetection />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

