import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Layers, Database, MessageSquare, Activity, LogOut, User } from "lucide-react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export default function Navbar({ onLogout }) {
  const location = useLocation();
  const currentPath = location.pathname;
  const [health, setHealth] = useState(null);

  // Read admin username from stored session
  const getAdminUser = () => {
    try {
      const session = JSON.parse(localStorage.getItem("oceanrag_admin_session") || "{}");
      return session.username || null;
    } catch {
      return null;
    }
  };
  const adminUser = getAdminUser();
  const isLoggedIn = !!adminUser;

  // Check backend health once when the frontend-backend connection is established
  useEffect(() => {
    let isMounted = true;
    const checkHealth = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/health`);
        const data = await res.json();
        if (isMounted) setHealth(data.status === "OK" ? "ok" : "degraded");
      } catch {
        if (isMounted) setHealth("down");
      }
    };
    checkHealth();
    return () => {
      isMounted = false;
    };
  }, []);

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
        <nav className="flex items-center gap-2 p-1 bg-white/5 rounded-full border border-white/5">
          <Link
            to="/admin/applications"
            className={`flex items-center gap-2 px-4 py-1.5 rounded-full text-xs md:text-sm font-medium transition duration-300 tracking-wide focus-visible:ring-2 focus-visible:ring-[#00D4FF] focus-visible:outline-none ${
              currentPath.startsWith("/admin") || currentPath.startsWith("/dashboard")
                ? "bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] shadow-[0_0_12px_rgba(0,212,255,0.4)]"
                : "text-slate-400 hover:text-white hover:bg-white/5"
            }`}
            data-testid="nav-dashboard"
          >
            <Database className="h-3.5 w-3.5" />
            <span>Admin Console</span>
          </Link>

          <Link
            to="/chat"
            className={`flex items-center gap-2 px-4 py-1.5 rounded-full text-xs md:text-sm font-medium transition duration-300 tracking-wide focus-visible:ring-2 focus-visible:ring-[#00D4FF] focus-visible:outline-none ${
              currentPath === "/chat"
                ? "bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] shadow-[0_0_12px_rgba(0,212,255,0.4)]"
                : "text-slate-400 hover:text-white hover:bg-white/5"
            }`}
            data-testid="nav-chat"
          >
            <MessageSquare className="h-3.5 w-3.5" />
            <span>Chat</span>
          </Link>
        </nav>

        {/* Right controls: user + logout + health */}
        <div className="flex items-center gap-4">
          {/* Health Status Indicator */}
          <div
            className="flex items-center gap-1.5 text-[10px] font-mono"
            title={`Backend health: ${health || "checking..."}`}
            data-testid="health-indicator"
          >
            <Activity className={`h-3.5 w-3.5 ${
              health === "ok" ? "text-emerald-400" : health === "down" ? "text-red-400" : "text-amber-400"
            }`} />
            <span className={`hidden sm:inline ${
              health === "ok" ? "text-emerald-400" : health === "down" ? "text-red-400" : "text-amber-400"
            }`}>
              {health === "ok" ? "OK" : health === "down" ? "OFFLINE" : "..."}
            </span>
          </div>

          {/* User + Logout (only when logged in) */}
          {isLoggedIn && (
            <div className="flex items-center gap-2 pl-3 border-l border-white/10" data-testid="user-menu">
              <User className="h-3.5 w-3.5 text-[#00D4FF]" />
              <span className="hidden md:inline text-xs font-semibold text-slate-200">{adminUser}</span>
              <button
                onClick={onLogout}
                className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-red-500/30 text-red-400 hover:bg-red-500/10 hover:text-red-300 transition text-xs font-semibold focus:outline-none"
                title="Logout"
                data-testid="logout-btn"
              >
                <LogOut className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}