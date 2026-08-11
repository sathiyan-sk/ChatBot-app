import React from "react";
import { Link, useLocation } from "react-router-dom";
import { MessageSquare, Database, Layers, LogOut } from "lucide-react";
import { toast } from "sonner";

export default function Navbar() {
  const location = useLocation();
  const currentPath = location.pathname;

  const handleLogout = () => {
    localStorage.removeItem("oceanrag_admin_session");
    toast.success("Logged out successfully.");
    setTimeout(() => {
      window.location.href = "/";
    }, 500);
  };

  const isAdminSession = localStorage.getItem("oceanrag_admin_session") !== null;

  return (
    <header className="sticky top-0 z-50 w-full px-4 pt-4 md:px-8 bg-transparent">
      <div 
        className="mx-auto max-w-6xl glassmorphism rounded-full px-6 py-3 flex items-center justify-between shadow-[0_4px_30px_rgba(0,0,0,0.3)]"
        data-testid="navbar-container"
      >
        {/* Brand Logo */}
        <Link 
          to="/" 
          className="flex items-center gap-2 group focus-visible:ring-2 focus-visible:ring-[#00D4FF] focus-visible:outline-none rounded"
          data-testid="nav-brand"
        >
          <div className="relative">
            <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-[#00D4FF] to-[#2563EB] opacity-70 blur-sm group-hover:opacity-100 transition duration-300"></div>
            <div className="relative bg-[#0B1221] p-1.5 rounded-full border border-white/10">
              <Layers className="h-5 w-5 text-[#00D4FF]" />
            </div>
          </div>
          <span className="font-semibold text-lg md:text-xl bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent group-hover:to-white transition duration-300 tracking-tight">
            RENAI<span className="text-[#00D4FF]">CHATBOT</span>
          </span>
        </Link>

        {/* Navigation Tabs (Glass Pills) */}
        {isAdminSession && (
          <nav className="flex items-center gap-2 p-1 bg-white/5 rounded-full border border-white/5">
            <Link
              to="/chat"
              className={`flex items-center gap-2 px-4 py-1.5 rounded-full text-xs md:text-sm font-medium transition duration-300 tracking-wide focus-visible:ring-2 focus-visible:ring-[#00D4FF] focus-visible:outline-none ${
                currentPath === "/chat" || currentPath === "/" || currentPath.startsWith("/dashboard")
                  ? "bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] shadow-[0_0_12px_rgba(0,212,255,0.4)]"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
              data-testid="nav-chat"
            >
              <MessageSquare className="h-3.5 w-3.5" />
              <span>Admin Console</span>
            </Link>
          </nav>
        )}

        {/* Logout action */}
        {isAdminSession ? (
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold text-red-400 border border-red-500/20 hover:bg-red-500/10 hover:text-red-300 transition duration-300 focus:outline-none cursor-pointer"
            data-testid="logout-btn"
          >
            <LogOut className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        ) : (
          <div className="flex items-center gap-2 text-xs text-slate-400 bg-white/5 px-3 py-1.5 rounded-full border border-white/10">
            <div className="h-2 w-2 rounded-full bg-blue-500 animate-pulse"></div>
            <span className="font-mono tracking-tight text-[10px]">Contract Secured</span>
          </div>
        )}
      </div>
    </header>
  );
}
