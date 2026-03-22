import React from "react";
import { Mail, Lock, ArrowRight, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";

const Login = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f172a] p-4 text-white">
      <div className="max-w-4xl w-full flex bg-[#1e293b] rounded-3xl overflow-hidden shadow-2xl border border-slate-700">
        {/* Left Side - Visual */}
        <div className="hidden md:flex w-1/2 bg-gradient-to-br from-blue-600 to-indigo-900 p-12 flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-2xl font-bold italic mb-6">
              <ShieldCheck size={32} /> DeepTrace
            </div>
            <h2 className="text-4xl font-bold leading-tight">
              Secure your digital <br /> authenticity.
            </h2>
          </div>
          <p className="text-blue-100 opacity-80 text-sm">
            Powered by advanced neural networks to distinguish human creativity
            from machine generation.
          </p>
        </div>

        {/* Right Side - Form */}
        <div className="w-full md:w-1/2 p-12">
          <h2 className="text-3xl font-bold mb-2">Welcome Back</h2>
          <p className="text-slate-400 mb-8">
            Enter your credentials to access the dashboard.
          </p>

          <form className="space-y-6">
            <div className="relative">
              <Mail
                className="absolute left-3 top-3.5 text-slate-500"
                size={20}
              />
              <input
                type="email"
                placeholder="Email Address"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl py-3 pl-12 pr-4 focus:ring-2 focus:ring-blue-500 outline-none transition"
              />
            </div>

            <div className="relative">
              <Lock
                className="absolute left-3 top-3.5 text-slate-500"
                size={20}
              />
              <input
                type="password"
                placeholder="Password"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl py-3 pl-12 pr-4 focus:ring-2 focus:ring-blue-500 outline-none transition"
              />
            </div>

            <button className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02]">
              Sign In <ArrowRight size={20} />
            </button>
          </form>

          <p className="mt-8 text-center text-slate-400 text-sm">
            Don't have an account?{" "}
            <Link to="/signup" className="text-blue-400 hover:underline">
              Create one free
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
