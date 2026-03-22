import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Login from "./page/auth/Login";
import Register from "./page/auth/Register";
import Dashboard from "./page/Dashboard";
import ImageDetection from "./page/ImageDetection";
import VideoDetection from "./page/VideoDetection";
import TextDetection from "./page/TextDetection";
import History from "./page/History";

function App() {
  return (
    <Router>
      <Routes>
        {/* Auth Pages (Full Screen, No Sidebar) */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Register />} />

        {/* Dashboard Pages (With Sidebar & Topbar) */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="detect-image" element={<ImageDetection />} />
          <Route path="detect-video" element={<VideoDetection />} />
          <Route path="detect-text" element={<TextDetection />} />
          <Route path="history" element={<History />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

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
