import React, { useState } from "react";
import { Lock, User, Layers, ShieldCheck, ArrowRight, Loader2 } from "lucide-react";
import { toast } from "sonner";

export default function Login({ onLoginSuccess }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password || isLoading) return;

    setIsLoading(true);
    
    // Hardcoded credentials checked securely by default
    if ((email === "admin" || email === "admin@example.com") && password === "admin123") {
      setTimeout(() => {
        setIsLoading(false);
        const userSession = {
          email: "admin@example.com",
          role: "admin",
          name: "RAG Administrator",
          token: "mock_jwt_token_oceanrag_2026"
        };
        localStorage.setItem("oceanrag_admin_session", JSON.stringify(userSession));
        onLoginSuccess(userSession);
        toast.success("Welcome back, Administrator!");
      }, 1200);
    } else {
      setTimeout(() => {
        setIsLoading(false);
        toast.error("Invalid administrator UserID or Password.");
      }, 800);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#040914] text-white px-4">
      {/* Decorative Blur Orbs */}
      <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-500/10 rounded-full filter blur-[80px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 right-1/4 w-72 h-72 bg-cyan-500/10 rounded-full filter blur-[80px] pointer-events-none"></div>

      <div className="w-full max-w-md" data-testid="login-container">
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="inline-flex p-3 bg-white/5 rounded-2xl border border-white/10 glow-cyan mb-4">
            <Layers className="h-8 w-8 text-[#00D4FF]" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            RENAI<span className="text-[#00D4FF]">ADMIN</span> Console
          </h1>
          <p className="text-slate-400 text-xs mt-2 font-medium">
            AI Knowledge Platform Administrator Portal
          </p>
        </div>

        {/* Login Form Box */}
        <div className="glassmorphism rounded-3xl p-8 border-white/10 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#2563EB] to-[#00D4FF]"></div>
          
          <div className="flex items-center gap-2 text-xs font-semibold text-[#00D4FF] mb-6 uppercase tracking-wider font-mono">
            <ShieldCheck className="h-4 w-4" />
            <span>Secure Access Control</span>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5" data-testid="login-form">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                UserID / Email
              </label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-500">
                  <User className="h-4 w-4" />
                </span>
                <input
                  type="text"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g. admin"
                  className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-sm rounded-xl pl-10 pr-4 py-3 outline-none transition-all duration-300 focus:ring-1 focus:ring-[#00D4FF]"
                  data-testid="login-email-input"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                Password
              </label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-500">
                  <Lock className="h-4 w-4" />
                </span>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-sm rounded-xl pl-10 pr-4 py-3 outline-none transition-all duration-300 focus:ring-1 focus:ring-[#00D4FF]"
                  data-testid="login-password-input"
                  required
                />
              </div>
            </div>

            {/* Quick Helper Credentials */}
            <div className="p-3 bg-white/5 rounded-xl border border-white/5 text-[11px] text-slate-400">
              <span className="font-semibold text-slate-300">Demo Credentials:</span><br />
              User ID: <code className="text-slate-200">admin</code> • Pass: <code className="text-slate-200">admin123</code>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full h-12 bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] hover:text-[#040914] font-bold text-xs tracking-widest uppercase rounded-xl transition duration-300 hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_15px_rgba(0,212,255,0.2)] flex items-center justify-center gap-2 cursor-pointer mt-2"
              data-testid="login-submit-btn"
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin text-[#040914]" />
                  <span>AUTHORIZING SESSION...</span>
                </>
              ) : (
                <>
                  <span>LOGIN CONTRACT</span>
                  <ArrowRight className="h-4 w-4 text-[#040914]" />
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
