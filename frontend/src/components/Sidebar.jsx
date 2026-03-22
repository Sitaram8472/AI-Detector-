import { Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Image,
  Video,
  FileText,
  History,
  LogOut,
  ShieldCheck,
} from "lucide-react";

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { name: "Dashboard", path: "/", icon: <LayoutDashboard size={20} /> },
    { name: "Image Detect", path: "/detect-image", icon: <Image size={20} /> },
    { name: "Video Detect", path: "/detect-video", icon: <Video size={20} /> },
    { name: "Text Detect", path: "/detect-text", icon: <FileText size={20} /> },
    { name: "History", path: "/history", icon: <History size={20} /> },
  ];

  return (
    <aside className="w-64 bg-[#0f172a] text-slate-300 flex flex-col border-r border-slate-800">
      <div className="p-6 flex items-center gap-3 text-white font-bold text-xl italic">
        <div className="bg-blue-600 p-1.5 rounded-lg">
          <ShieldCheck size={24} />
        </div>
        DeepTrace
      </div>

      <nav className="flex-1 px-4 space-y-2 mt-4">
        {menuItems.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
              location.pathname === item.path
                ? "bg-blue-600 text-white shadow-lg shadow-blue-500/20"
                : "hover:bg-slate-800 hover:text-white"
            }`}
          >
            {item.icon}
            <span className="font-medium">{item.name}</span>
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <button className="flex items-center gap-3 w-full px-4 py-3 text-red-400 hover:bg-red-500/10 rounded-xl transition-colors">
          <LogOut size={20} />
          <span className="font-medium">Logout</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
