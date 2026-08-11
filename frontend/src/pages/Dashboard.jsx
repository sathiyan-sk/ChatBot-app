import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { Plus, Database, Layers, ArrowRight, Loader2, FileText, Cpu, Clock } from "lucide-react";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8001";
const API = `${BACKEND_URL}/api`;

export default function Dashboard() {
  const [apps, setApps] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newAppName, setNewAppName] = useState("");
  const [newAppDesc, setNewAppDesc] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchApps = async () => {
    try {
      const response = await axios.get(`${API}/applications`);
      setApps(response.data);
    } catch (e) {
      console.error(e);
      toast.error("Failed to fetch applications from RAG backend.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchApps();
  }, []);

  const handleCreateApp = async (e) => {
    e.preventDefault();
    if (!newAppName.trim() || isSubmitting) return;

    setIsSubmitting(true);
    try {
      const response = await axios.post(`${API}/applications`, {
        name: newAppName,
        description: newAppDesc,
        model: "llama3:latest",
        system_prompt: "You are a helpful RAG-powered knowledge assistant."
      });
      toast.success(`Application "${newAppName}" created successfully!`);
      setNewAppName("");
      setNewAppDesc("");
      setShowCreateModal(false);
      fetchApps();
    } catch (e) {
      console.error(e);
      toast.error("Failed to create application.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="max-w-6xl mx-auto px-4 md:px-8 py-8">
      {/* Top Welcome Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
        <div>
          <h1 className="text-3xl md:text-4xl font-semibold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            Applications Directory
          </h1>
          <p className="text-slate-400 text-sm mt-1.5 leading-relaxed max-w-xl">
            Register namespaces, provision embeddable chat widgets, and synchronize FAISS document indices within isolated application contexts.
          </p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] font-semibold text-xs tracking-wider uppercase hover:scale-[1.03] active:scale-[0.97] transition duration-300 shadow-[0_0_15px_rgba(0,212,255,0.2)] cursor-pointer"
          data-testid="create-app-trigger"
        >
          <Plus className="h-4 w-4" />
          <span>Provision Application</span>
        </button>
      </div>

      {/* Directory Grid */}
      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="h-8 w-8 text-[#00D4FF] animate-spin" />
        </div>
      ) : apps.length === 0 ? (
        <div className="text-center py-20 border border-dashed border-white/5 rounded-3xl bg-white/2">
          <Database className="h-12 w-12 text-slate-600 mx-auto mb-4" />
          <h3 className="font-semibold text-base text-slate-300">No applications found</h3>
          <p className="text-slate-500 text-xs mt-1.5 max-w-md mx-auto leading-relaxed">
            Create an isolated namespace to begin uploading documents, customizing styles, and testing Retrieval Augmented Generation parameters.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="applications-grid">
          {apps.map((app) => (
            <Link
              key={app.id}
              to={`/dashboard/${app.id}`}
              className="group glassmorphism rounded-2xl p-6 border-white/10 hover:border-[#00D4FF]/30 hover:shadow-[0_0_20px_rgba(0,212,255,0.1)] transition-all duration-300 flex flex-col justify-between h-56 relative overflow-hidden"
              data-testid={`app-card-${app.id}`}
            >
              {/* Highlight top accent */}
              <div className="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-[#2563EB]/40 to-[#00D4FF]/40 group-hover:from-[#2563EB] group-hover:to-[#00D4FF] transition-all duration-300"></div>

              <div>
                <div className="flex items-center justify-between gap-3 mb-4">
                  <div className="p-2.5 bg-white/5 rounded-xl border border-white/10 text-[#00D4FF]">
                    <Layers className="h-5 w-5" />
                  </div>
                  <span className="font-mono text-[9px] text-slate-500 bg-white/5 px-2.5 py-1 rounded-full border border-white/5 uppercase tracking-wide">
                    ID: {app.id}
                  </span>
                </div>

                <h3 className="font-semibold text-base text-white group-hover:text-[#00D4FF] transition duration-200 truncate">
                  {app.name}
                </h3>
                <p className="text-slate-400 text-xs mt-1.5 line-clamp-2 leading-relaxed">
                  {app.description || "No description provided."}
                </p>
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-white/5 text-[10px] text-slate-500 font-medium">
                <div className="flex items-center gap-1.5">
                  <Cpu className="h-3 w-3 text-slate-400" />
                  <span>{app.model}</span>
                </div>
                <div className="flex items-center gap-1 hover:text-white transition duration-200 text-[#00D4FF] font-semibold">
                  <span>Manage</span>
                  <ArrowRight className="h-3 w-3 translate-x-0 group-hover:translate-x-1 transition duration-200" />
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* Create Modal Panel (Glass Layer Overlay) */}
      {showCreateModal && (
        <div 
          className="fixed inset-0 z-50 bg-[#040914]/80 backdrop-blur-md flex items-center justify-center p-4 animate-fadeIn"
          data-testid="create-app-modal"
        >
          <div className="w-full max-w-md glassmorphism rounded-3xl border-white/10 p-7 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#2563EB] to-[#00D4FF]"></div>
            
            <h3 className="font-semibold text-lg text-white mb-1 tracking-tight">
              Provision Application Namespace
            </h3>
            <p className="text-slate-400 text-xs mb-5">
              Isolated context mapping specific knowledge bases.
            </p>

            <form onSubmit={handleCreateApp} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Application Name
                </label>
                <input
                  type="text"
                  value={newAppName}
                  onChange={(e) => setNewAppName(e.target.value)}
                  placeholder="e.g. FAQ Support Assistant"
                  className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Description
                </label>
                <textarea
                  value={newAppDesc}
                  onChange={(e) => setNewAppDesc(e.target.value)}
                  placeholder="Describe the application scope..."
                  rows={3}
                  className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition resize-none"
                  required
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-white/5">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/5 transition text-xs font-semibold focus:outline-none"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting || !newAppName.trim()}
                  className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] font-bold text-xs tracking-wider uppercase hover:scale-[1.02] active:scale-[0.98] transition shadow-md focus:outline-none cursor-pointer"
                  data-testid="create-app-submit"
                >
                  {isSubmitting ? "Provisioning..." : "Confirm Provision"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}
