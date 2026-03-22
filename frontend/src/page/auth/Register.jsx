import React from "react";
import { User, Mail, Lock, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";

const Register = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f172a] p-4 text-white font-sans">
      <div className="max-w-md w-full bg-[#1e293b] p-10 rounded-3xl shadow-2xl border border-slate-700 relative overflow-hidden">
        {/* Background glow effect */}
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-blue-600/20 blur-3xl rounded-full"></div>

        <div className="flex justify-center mb-6">
          <div className="bg-blue-600 p-3 rounded-2xl shadow-lg shadow-blue-500/30">
            <ShieldCheck size={32} />
          </div>
        </div>

        <h2 className="text-3xl font-bold text-center mb-2">Join DeepTrace</h2>
        <p className="text-slate-400 text-center mb-8 text-sm">
          Start detecting AI content in seconds.
        </p>

        <form className="space-y-5">
          <div className="relative">
            <User className="absolute left-3 top-3 text-slate-500" size={18} />
            <input
              type="text"
              placeholder="Full Name"
              className="w-full bg-slate-900/50 border border-slate-700 rounded-xl py-3 pl-11 outline-none focus:border-blue-500"
            />
          </div>
          <div className="relative">
            <Mail className="absolute left-3 top-3 text-slate-500" size={18} />
            <input
              type="email"
              placeholder="Email"
              className="w-full bg-slate-900/50 border border-slate-700 rounded-xl py-3 pl-11 outline-none focus:border-blue-500"
            />
          </div>
          <div className="relative">
            <Lock className="absolute left-3 top-3 text-slate-500" size={18} />
            <input
              type="password"
              placeholder="Password"
              className="w-full bg-slate-900/50 border border-slate-700 rounded-xl py-3 pl-11 outline-none focus:border-blue-500"
            />
          </div>

          <button className="w-full py-4 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl font-bold shadow-lg shadow-blue-500/20 hover:opacity-90 transition">
            Create Account
          </button>
        </form>

        <p className="mt-6 text-center text-slate-400 text-sm">
          Already a member?{" "}
          <Link to="/login" className="text-blue-400 font-semibold">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
