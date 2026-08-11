import React, { useState, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Login from "@/pages/Login";
import Dashboard from "@/pages/Dashboard";
import ApplicationDetail from "@/pages/ApplicationDetail";
import { Toaster } from "sonner";

function App() {
  const [session, setSession] = useState(null);
  const [checkingSession, setCheckingSession] = useState(true);

  useEffect(() => {
    const saved = localStorage.getItem("oceanrag_admin_session");
    if (saved) {
      try {
        setSession(JSON.parse(saved));
      } catch (e) {
        console.error("Failed to restore session", e);
      }
    }
    setCheckingSession(false);
  }, []);

  const handleLoginSuccess = (userSession) => {
    setSession(userSession);
  };

  if (checkingSession) {
    return (
      <div className="min-h-screen bg-[#040914] flex items-center justify-center text-white">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-4 border-t-cyan-400 border-r-transparent border-slate-700 rounded-full animate-spin"></div>
          <p className="text-xs text-slate-400 font-mono tracking-wide">VERIFYING ADMIN CONTEXT...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <BrowserRouter>
        {/* Global Toaster for beautiful toast feedback */}
        <Toaster richColors closeButton theme="dark" />
        
        {/* Floating Premium Top Nav Pill */}
        <Navbar />
        
        {/* Router Context guarding by default */}
        <div className="flex-1 w-full relative">
          <Routes>
            {session ? (
              <>
                <Route path="/chat" element={<Dashboard />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/dashboard/:id" element={<ApplicationDetail />} />
                <Route path="*" element={<Navigate to="/chat" replace />} />
              </>
            ) : (
              <>
                <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />
                <Route path="*" element={<Navigate to="/login" replace />} />
              </>
            )}
          </Routes>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;
