import React from "react";
import { Image, Video, FileText, Activity } from "lucide-react";
import { Link } from "react-router-dom";

const Dashboard = () => {
  const tools = [
    {
      title: "Image Detection",
      icon: <Image />,
      path: "/detect-image",
      desc: "Scan for AI-generated faces or art.",
    },
    {
      title: "Video Detection",
      icon: <Video />,
      path: "/detect-video",
      desc: "Analyze deepfake movements and frames.",
    },
    {
      title: "Text Analysis",
      icon: <FileText />,
      path: "/detect-text",
      desc: "Check for GPT or LLM patterns.",
    },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-2">
        DeepTrace Dashboard
      </h1>
      <p className="text-gray-500 mb-8">
        Welcome back. Select a tool to begin analyzing content.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {tools.map((tool) => (
          <Link
            to={tool.path}
            key={tool.title}
            className="p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
          >
            <div className="text-blue-600 mb-4">{tool.icon}</div>
            <h2 className="text-xl font-semibold mb-2">{tool.title}</h2>
            <p className="text-gray-600 text-sm">{tool.desc}</p>
          </Link>
        ))}
      </div>

      {/* Recent Activity Placeholder */}
      <div className="mt-10 p-6 bg-white rounded-xl shadow-sm border border-gray-100">
        <div className="flex items-center gap-2 mb-4 font-semibold">
          <Activity size={20} className="text-green-500" />
          <span>Recent Scans</span>
        </div>
        <p className="text-gray-400 text-sm">No recent scans found.</p>
      </div>
    </div>
  );
};

export default Dashboard;
