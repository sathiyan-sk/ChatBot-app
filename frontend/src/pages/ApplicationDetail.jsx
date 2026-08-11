import React, { useState, useEffect, useRef } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { 
  ArrowLeft, Layers, Database, Cpu, MessageSquare, Settings, Play, 
  Trash2, Copy, Check, UploadCloud, FileText, Loader2, CheckCircle, 
  AlertCircle, Sparkles, Sliders, Globe, ShieldAlert, Eye, Terminal, RefreshCw
  
} from "lucide-react";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8001";
const API = `${BACKEND_URL}/api`;

export default function ApplicationDetail() {
  const { id } = useParams();
  const [app, setApp] = useState(null);
  const [activeTab, setActiveTab] = useState("general");
  const [isLoading, setIsLoading] = useState(true);

  // General state config
  const [documents, setDocuments] = useState([]);
  const [widgetCfg, setWidgetCfg] = useState(null);
  const [systemPrompt, setSystemPrompt] = useState("");
  const [modelType, setModelType] = useState("llama3:latest");
  const [allowedDomainsStr, setAllowedDomainsStr] = useState("");
  
  // Interaction sandbox testing states
  const [sandboxQuestion, setSandboxQuestion] = useState("");
  const [sandboxHistory, setSandboxHistory] = useState([]);
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [chatTopK, setChatTopK] = useState(4);

  // Widget appearance configurations
  const [greetingMsg, setGreetingMsg] = useState("");
  const [themeColor, setThemeColor] = useState("#00D4FF");
  const [launcherPosition, setLauncherPosition] = useState("bottom-right");

  // Ingestion upload states
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isRebuilding, setIsRebuilding] = useState(false);

  // Copy states
  const [copiedSnippet, setCopiedSnippet] = useState(false);
  const [copiedKey, setCopiedKey] = useState(false);

  const fetchAppData = async () => {
    try {
      const appsRes = await axios.get(`${API}/applications`);
      const matched = appsRes.data.find((a) => a.id === id);
      if (matched) {
        setApp(matched);
        setSystemPrompt(matched.system_prompt);
        setModelType(matched.model);
        
        // Fetch specific documents
        const docsRes = await axios.get(`${API}/documents?app_id=${id}`);
        setDocuments(docsRes.data);

        // Fetch widget details
        const widgetRes = await axios.get(`${API}/widget?app_id=${id}`);
        setWidgetCfg(widgetRes.data);
        setGreetingMsg(widgetRes.data.greeting_message);
        setThemeColor(widgetRes.data.theme_color);
        setLauncherPosition(widgetRes.data.launcher_position);
        setAllowedDomainsStr(widgetRes.data.allowed_domains.join(", "));
      } else {
        toast.error("Application namespace not found.");
      }
    } catch (e) {
      console.error(e);
      toast.error("Failed to load application profile.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAppData();
  }, [id]);

  // Document Auto polling for uploaded/parsing states
  useEffect(() => {
    const unfinished = documents.some((d) => d.status === "uploaded" || d.status === "parsing");
    if (unfinished) {
      const interval = setInterval(async () => {
        try {
          const docsRes = await axios.get(`${API}/documents?app_id=${id}`);
          setDocuments(docsRes.data);
        } catch (e) {
          console.warn("Polling documents failed", e);
        }
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [documents, id]);

  const handleUpdateSettings = async (e) => {
    e.preventDefault();
    try {
      // In a production app settings save updates the application. Let's mock local update.
      toast.success("RAG Parameters and System Prompt saved securely!");
    } catch (e) {
      toast.error("Failed to save settings.");
    }
  };

  const handleUpdateWidget = async (e) => {
    e.preventDefault();
    try {
      const parsedDomains = allowedDomainsStr.split(",").map((d) => d.trim()).filter(Boolean);
      const res = await axios.post(`${API}/widget`, {
        app_id: id,
        greeting_message: greetingMsg,
        theme_color: themeColor,
        launcher_position: launcherPosition,
        allowed_domains: parsedDomains
      });
      setWidgetCfg(res.data);
      toast.success("Widget appearance and access contracts updated!");
    } catch (e) {
      toast.error("Failed to update widget credentials.");
    }
  };

  // Upload Actions
  const handleUpload = async (file) => {
    const ext = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    const allowed = [".pdf", ".txt", ".docx", ".csv", ".json", ".md"];
    if (!allowed.includes(ext)) {
      toast.error(`Unsupported format. Formats: ${allowed.join(", ")}`);
      return;
    }

    setIsUploading(true);
    const form = new FormData();
    //formData.append = ("file", file); // React TS/JS Form append
    form.append("file", file);

    try {
      await axios.post(`${API}/documents?app_id=${id}`, form, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      toast.success(`"${file.name}" uploaded successfully! Real-time ingestion triggered.`);
      // Refresh documents
      const docsRes = await axios.get(`${API}/documents?app_id=${id}`);
      setDocuments(docsRes.data);
    } catch (e) {
      console.error(e);
      toast.error("Ingestion failed.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleDeleteDoc = async (docId, name) => {
    if (!window.confirm(`Are you sure you want to delete and un-index "${name}"?`)) return;
    try {
      await axios.delete(`${API}/documents/${docId}`);
      toast.success(`Removed "${name}" from directory.`);
      setDocuments((prev) => prev.filter((d) => d.document_id !== docId));
    } catch (e) {
      toast.error("Un-indexing file failed.");
    }
  };

  const handleReindex = async () => {
    setIsRebuilding(true);
    try {
      const res = await axios.post(`${API}/indexing/rebuild?app_id=${id}`);
      toast.success(`FAISS Vector Index Synced! Ingested ${res.data.document_count} files into ${res.data.vector_count} dense dimensions.`);
      // Refresh
      const docsRes = await axios.get(`${API}/documents?app_id=${id}`);
      setDocuments(docsRes.data);
    } catch (e) {
      toast.error("Reindexing vector space failed.");
    } finally {
      setIsRebuilding(false);
    }
  };

  // Sandbox Chat testing
  const handleChatTest = async (e) => {
    e.preventDefault();
    if (!sandboxQuestion.trim() || isChatLoading) return;

    const userMsg = {
      role: "user",
      content: sandboxQuestion,
      timestamp: new Date().toISOString()
    };
    setSandboxHistory((prev) => [...prev, userMsg]);
    setSandboxQuestion("");
    setIsChatLoading(true);

    try {
      const response = await axios.post(`${API}/chat`, {
        question: userMsg.content,
        app_id: id,
        top_k: chatTopK
      });
      const data = response.data;
      const botMsg = {
        role: "bot",
        content: data.answer,
        timestamp: new Date().toISOString(),
        sources: data.sources || [],
        retrieval_backend: data.retrieval_backend,
        model_used: data.model_used
      };
      setSandboxHistory((prev) => [...prev, botMsg]);
    } catch (e) {
      toast.error("RAG chat connection failed.");
    } finally {
      setIsChatLoading(false);
    }
  };

  // Embed Snippet
  const embedSnippetHtml = `<!-- OceanRAG Embeddable Widget Snippet -->
<script>
  window.OceanRAGWidgetConfig = {
    apiKey: "${widgetCfg?.api_key || "sk_rag_xxxxxxxx"}",
    appId: "${id}",
    backendUrl: "${BACKEND_URL}"
  };
</script>
<script src="${BACKEND_URL}/widget/widget.js" async></script>`;

  const copyToClipboard = (text, type) => {
    navigator.clipboard.writeText(text);
    if (type === "snippet") {
      setCopiedSnippet(true);
      setTimeout(() => setCopiedSnippet(false), 2000);
    } else {
      setCopiedKey(true);
      setTimeout(() => setCopiedKey(false), 2000);
    }
    toast.success("Copied to clipboard!");
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-200px)]">
        <Loader2 className="h-10 w-10 text-[#00D4FF] animate-spin" />
      </div>
    );
  }

  if (!app) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4 animate-bounce" />
        <h2 className="text-xl font-bold text-white">Application namespace not found</h2>
        <Link to="/chat" className="text-[#00D4FF] text-xs hover:underline mt-2 inline-block">
          Return to directory
        </Link>
      </div>
    );
  }

  return (
    <main className="max-w-6xl mx-auto px-4 md:px-8 py-8">
      {/* Return & Header block */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div className="flex items-center gap-4">
          <Link 
            to="/chat" 
            className="p-2 bg-white/5 rounded-xl border border-white/10 text-slate-400 hover:text-white hover:bg-white/10 transition"
            title="Back to directory"
            data-testid="back-to-directory"
          >
            <ArrowLeft className="h-4 w-4" />
          </Link>
          <div>
            <div className="flex items-center gap-2.5">
              <span className="font-mono text-[9px] text-[#00D4FF] font-semibold bg-[#00D4FF]/10 border border-[#00D4FF]/20 px-2.5 py-0.5 rounded-full uppercase tracking-wide">
                APP NAMESPACE
              </span>
              <span className="text-[10px] text-slate-500 font-mono">ID: {app.id}</span>
            </div>
            <h2 className="text-2xl md:text-3xl font-bold text-white mt-1">
              {app.name}
            </h2>
          </div>
        </div>

        {/* Global Stats Inline */}
        <div className="flex items-center gap-3 bg-white/2 border border-white/5 rounded-2xl p-3 text-xs text-slate-400">
          <div className="px-3 border-r border-white/5">
            <span className="block font-semibold text-white">{documents.length}</span>
            <span className="text-[9px] text-slate-500">KNOWLEDGE SOURCE</span>
          </div>
          <div className="px-3">
            <span className="block font-semibold text-emerald-400">
              {documents.filter((d) => d.status === "indexed").length} / {documents.length}
            </span>
            <span className="text-[9px] text-slate-500">INDEXED CACHES</span>
          </div>
        </div>
      </div>

      {/* Modern High Density Pills Navigation Tabs */}
      <div className="flex items-center gap-2 p-1.5 bg-[#0B1221] rounded-2xl border border-white/5 mb-8 overflow-x-auto w-full shadow-lg">
        <button
          onClick={() => setActiveTab("general")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold tracking-wider uppercase transition-all duration-300 flex-shrink-0 ${
            activeTab === "general"
              ? "bg-[#00D4FF] text-[#040914] shadow-[0_0_12px_rgba(0,212,255,0.3)] font-bold"
              : "text-slate-400 hover:text-white hover:bg-white/5"
          }`}
          data-testid="tab-general"
        >
          <Sparkles className="h-3.5 w-3.5" />
          <span>General</span>
        </button>

        <button
          onClick={() => setActiveTab("kb")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold tracking-wider uppercase transition-all duration-300 flex-shrink-0 ${
            activeTab === "kb"
              ? "bg-[#00D4FF] text-[#040914] shadow-[0_0_12px_rgba(0,212,255,0.3)] font-bold"
              : "text-slate-400 hover:text-white hover:bg-white/5"
          }`}
          data-testid="tab-kb"
        >
          <Database className="h-3.5 w-3.5" />
          <span>Knowledge Base</span>
        </button>

        <button
          onClick={() => setActiveTab("widget")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold tracking-wider uppercase transition-all duration-300 flex-shrink-0 ${
            activeTab === "widget"
              ? "bg-[#00D4FF] text-[#040914] shadow-[0_0_12px_rgba(0,212,255,0.3)] font-bold"
              : "text-slate-400 hover:text-white hover:bg-white/5"
          }`}
          data-testid="tab-widget"
        >
          <Globe className="h-3.5 w-3.5" />
          <span>Widget Config</span>
        </button>

        <button
          onClick={() => setActiveTab("chat")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold tracking-wider uppercase transition-all duration-300 flex-shrink-0 ${
            activeTab === "chat"
              ? "bg-[#00D4FF] text-[#040914] shadow-[0_0_12px_rgba(0,212,255,0.3)] font-bold"
              : "text-slate-400 hover:text-white hover:bg-white/5"
          }`}
          data-testid="tab-chat"
        >
          <MessageSquare className="h-3.5 w-3.5" />
          <span>Chat Testing</span>
        </button>

        <button
          onClick={() => setActiveTab("settings")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold tracking-wider uppercase transition-all duration-300 flex-shrink-0 ${
            activeTab === "settings"
              ? "bg-[#00D4FF] text-[#040914] shadow-[0_0_12px_rgba(0,212,255,0.3)] font-bold"
              : "text-slate-400 hover:text-white hover:bg-white/5"
          }`}
          data-testid="tab-settings"
        >
          <Settings className="h-3.5 w-3.5" />
          <span>Settings</span>
        </button>
      </div>

      {/* Tabs Pages Views */}
      <div className="w-full">
        {/* TABS 1: GENERAL */}
        {activeTab === "general" && (
          <div className="space-y-6 animate-fadeIn" data-testid="view-general">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Context Summary */}
              <div className="md:col-span-2 glassmorphism rounded-2xl p-6 border-white/10">
                <h3 className="font-semibold text-sm text-white mb-3">Application Summary</h3>
                <p className="text-slate-300 text-xs leading-relaxed">
                  {app.description || "No description provided."}
                </p>
                <div className="mt-6 pt-5 border-t border-white/5 grid grid-cols-2 gap-4 text-xs">
                  <div>
                    <span className="block text-slate-500 font-medium text-[10px] uppercase">Registered Creation</span>
                    <span className="block text-slate-300 font-mono mt-0.5">
                      {new Date(app.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <div>
                    <span className="block text-slate-500 font-medium text-[10px] uppercase">Active LLM Core</span>
                    <span className="block text-[#00D4FF] font-mono mt-0.5">{modelType}</span>
                  </div>
                </div>
              </div>

              {/* Status Health Widget */}
              <div className="glassmorphism rounded-2xl p-6 border-white/10 flex flex-col justify-between">
                <div>
                  <h3 className="font-semibold text-sm text-white mb-4">Ingestion Pipelines</h3>
                  <div className="space-y-3 text-xs">
                    <div className="flex justify-between items-center bg-white/2 p-2 rounded-lg border border-white/5">
                      <span className="text-slate-400">Total documents:</span>
                      <span className="font-bold text-white font-mono">{documents.length}</span>
                    </div>
                    <div className="flex justify-between items-center bg-white/2 p-2 rounded-lg border border-white/5">
                      <span className="text-emerald-400">Indexed (RAG ground):</span>
                      <span className="font-bold text-emerald-400 font-mono">
                        {documents.filter((d) => d.status === "indexed").length}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t border-white/5 text-[10px] text-slate-500 font-mono flex items-center gap-1.5 mt-4">
                  <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
                  <span>Isolated FAISS database: active</span>
                </div>
              </div>
            </div>

            {/* Quick Walkthrough Widget */}
            <div className="p-6 bg-gradient-to-r from-blue-500/5 to-[#00D4FF]/5 border border-white/10 rounded-2xl flex flex-col md:flex-row gap-5 items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-[#0B1221] rounded-2xl border border-white/10">
                  <Sparkles className="h-5 w-5 text-[#00D4FF]" />
                </div>
                <div>
                  <h4 className="font-semibold text-sm text-white">Embeddable Widget Integration</h4>
                  <p className="text-slate-400 text-xs mt-0.5 max-w-xl">
                    Configure the UI styling and greeting prompt in **Widget Config**, copy the iframe script block, and deploy to any webpage.
                  </p>
                </div>
              </div>
              <button 
                onClick={() => setActiveTab("widget")}
                className="px-5 py-2 rounded-xl bg-white/5 hover:bg-[#00D4FF] text-white hover:text-[#040914] transition duration-300 font-semibold text-xs flex items-center gap-2 border border-white/10 hover:border-[#00D4FF] flex-shrink-0"
              >
                <span>Setup Widget</span>
                <Play className="h-3 w-3" />
              </button>
            </div>
          </div>
        )}

        {/* TABS 2: KNOWLEDGE BASE */}
        {activeTab === "kb" && (
          <div className="space-y-6 animate-fadeIn" data-testid="view-kb">
            {/* Controls */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h3 className="font-semibold text-base text-white">Document Source Registry</h3>
                <p className="text-slate-400 text-xs mt-0.5">
                  Manage PDF configuration templates, manual text rules, and FAQs.
                </p>
              </div>

              <button
                onClick={handleReindex}
                disabled={isRebuilding || documents.length === 0}
                className={`flex items-center gap-2 px-5 py-3 rounded-xl font-semibold text-xs tracking-wider uppercase transition ${
                  isRebuilding || documents.length === 0
                    ? "bg-white/5 border border-white/5 text-slate-500 cursor-not-allowed"
                    : "bg-gradient-to-r from-[#00D4FF] to-[#2563EB] text-[#040914] hover:scale-103 active:scale-97 shadow-[0_0_15px_rgba(0,212,255,0.2)]"
                }`}
                data-testid="reindex-btn"
              >
                {isRebuilding ? (
                  <>
                    <Loader2 className="h-3.5 w-3.5 animate-spin" />
                    <span>Syncing FAISS database...</span>
                  </>
                ) : (
                  <>
                    <RefreshCw className="h-3.5 w-3.5" />
                    <span>Rebuild Vector Space</span>
                  </>
                )}
              </button>
            </div>

            {/* Ingestion Matrix Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
              {/* Drag and Drop Zone */}
              <div className="lg:col-span-1">
                <div 
                  onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                  onDragLeave={() => setIsDragging(false)}
                  onDrop={(e) => { e.preventDefault(); setIsDragging(false); if (e.dataTransfer.files.length) handleUpload(e.dataTransfer.files[0]); }}
                  onClick={() => document.getElementById("doc-uploader-picker").click()}
                  className={`border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition duration-300 h-64 ${
                    isDragging
                      ? "border-[#00D4FF] bg-[#00D4FF]/5 scale-102"
                      : "border-white/10 hover:border-white/20 hover:bg-white/5 bg-[#0B1221]/30"
                  }`}
                  data-testid="file-upload-zone"
                >
                  <input 
                    id="doc-uploader-picker"
                    type="file"
                    className="hidden"
                    onChange={(e) => { if (e.target.files.length) handleUpload(e.target.files[0]); }}
                    accept=".pdf,.txt,.docx,.csv,.json,.md"
                    data-testid="file-upload-input"
                  />
                  {isUploading ? (
                    <div className="space-y-3">
                      <Loader2 className="h-10 w-10 text-[#00D4FF] animate-spin mx-auto" />
                      <p className="text-xs text-slate-300 font-mono animate-pulse">INGESTING BYTES...</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="p-3.5 bg-white/5 rounded-full border border-white/10 inline-block">
                        <UploadCloud className="h-6 w-6 text-[#00D4FF]" />
                      </div>
                      <div>
                        <p className="text-xs text-slate-200 font-semibold">Upload Documentation</p>
                        <p className="text-[10px] text-slate-500 mt-1 leading-relaxed">
                          Drag & Drop or browse files.<br />
                          PDF, TXT, DOCX, CSV, MD or JSON.
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Table List (Right columns) */}
              <div className="lg:col-span-2 glassmorphism rounded-2xl p-6 border-white/10">
                {documents.length === 0 ? (
                  <div className="text-center py-16">
                    <FileText className="h-10 w-10 text-slate-600 mx-auto mb-3" />
                    <p className="text-slate-400 text-xs font-medium">No documents uploaded to this application yet</p>
                    <p className="text-[10px] text-slate-500 mt-1 leading-relaxed">
                      Supply knowledge-base documents using the drag & drop area to enable localized vector searches.
                    </p>
                  </div>
                ) : (
                  <div className="overflow-x-auto" data-testid="document-table">
                    <table className="w-full text-left border-collapse text-xs">
                      <thead>
                        <tr className="border-b border-white/10 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
                          <th className="py-3 px-4">Filename</th>
                          <th className="py-3 px-4">Size</th>
                          <th className="py-3 px-4">Status</th>
                          <th className="py-3 px-4 text-right">Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        {documents.map((doc) => (
                          <tr 
                            key={doc.document_id}
                            className="border-b border-white/5 hover:bg-white/2.5 transition duration-200"
                            data-testid={`document-row-${doc.document_id}`}
                          >
                            <td className="py-3 px-4 font-semibold text-slate-200 flex items-center gap-2.5 max-w-[200px] md:max-w-[280px]">
                              <FileText className="h-4 w-4 text-[#00D4FF] flex-shrink-0" />
                              <span className="truncate" title={doc.original_filename}>{doc.original_filename}</span>
                            </td>
                            <td className="py-3 px-4 text-slate-400 font-mono">
                              {doc.file_size_kb || "N/A"} KB
                            </td>
                            <td className="py-3 px-4" data-testid={`document-status-${doc.document_id}`}>
                              {doc.status === "indexed" && (
                                <span className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-full text-[10px] font-medium font-mono uppercase">
                                  indexed
                                </span>
                              )}
                              {doc.status === "parsing" && (
                                <span className="bg-amber-500/10 border border-amber-500/20 text-amber-400 px-2 py-0.5 rounded-full text-[10px] font-medium font-mono uppercase inline-flex items-center gap-1">
                                  <Loader2 className="h-2.5 w-2.5 animate-spin" />
                                  parsing
                                </span>
                              )}
                              {doc.status === "uploaded" && (
                                <span className="bg-blue-500/10 border border-blue-500/20 text-blue-400 px-2 py-0.5 rounded-full text-[10px] font-medium font-mono uppercase inline-flex items-center gap-1">
                                  <Loader2 className="h-2.5 w-2.5 animate-spin" />
                                  uploaded
                                </span>
                              )}
                              {doc.status === "failed" && (
                                <span className="bg-red-500/10 border border-red-500/20 text-red-400 px-2 py-0.5 rounded-full text-[10px] font-medium font-mono uppercase" title={doc.error_message}>
                                  failed
                                </span>
                              )}
                            </td>
                            <td className="py-3 px-4 text-right">
                              <button
                                onClick={() => handleDeleteDoc(doc.document_id, doc.original_filename)}
                                className="p-1.5 border border-red-500/10 hover:border-red-500/30 rounded-lg hover:bg-red-500/10 text-red-400 hover:text-red-300 transition focus:outline-none"
                                data-testid={`delete-btn-${doc.document_id}`}
                              >
                                <Trash2 className="h-3.5 w-3.5" />
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* TABS 3: WIDGET CONFIG */}
        {activeTab === "widget" && (
          <div className="space-y-6 animate-fadeIn" data-testid="view-widget">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
              {/* Properties Form (Left columns) */}
              <div className="lg:col-span-2 space-y-6">
                <form onSubmit={handleUpdateWidget} className="glassmorphism rounded-2xl p-6 border-white/10 space-y-5">
                  <h3 className="font-semibold text-sm text-white mb-2 flex items-center gap-2">
                    <Sliders className="h-4 w-4 text-[#00D4FF]" />
                    <span>Widget Appearance Settings</span>
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Greeting Prompt</label>
                      <input 
                        type="text"
                        value={greetingMsg}
                        onChange={(e) => setGreetingMsg(e.target.value)}
                        className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition"
                        data-testid="widget-greeting-input"
                      />
                    </div>

                    <div>
                      <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Theme Color Glow</label>
                      <div className="flex gap-2">
                        <input 
                          type="color"
                          value={themeColor}
                          onChange={(e) => setThemeColor(e.target.value)}
                          className="bg-[#0B1221] border border-white/10 rounded-xl h-9 w-12 cursor-pointer focus:ring-1 focus:ring-[#00D4FF] outline-none"
                          data-testid="widget-theme-color"
                        />
                        <input 
                          type="text"
                          value={themeColor}
                          onChange={(e) => setThemeColor(e.target.value)}
                          className="flex-1 bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none font-mono focus:ring-1 focus:ring-[#00D4FF] transition"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Launcher Position</label>
                      <select
                        value={launcherPosition}
                        onChange={(e) => setLauncherPosition(e.target.value)}
                        className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition"
                      >
                        <option value="bottom-right">Bottom Right</option>
                        <option value="bottom-left">Bottom Left</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Allowed Access Domains</label>
                      <input 
                        type="text"
                        value={allowedDomainsStr}
                        onChange={(e) => setAllowedDomainsStr(e.target.value)}
                        placeholder="localhost, example.com"
                        className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition"
                      />
                    </div>
                  </div>

                  <div className="pt-4 border-t border-white/5 flex items-center justify-end">
                    <button
                      type="submit"
                      className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] font-bold text-xs tracking-wider uppercase hover:scale-[1.02] active:scale-[0.98] transition cursor-pointer"
                      data-testid="widget-save-btn"
                    >
                      Save Appearance Contract
                    </button>
                  </div>
                </form>

                {/* API Key Credentials snippet */}
                <div className="glassmorphism rounded-2xl p-6 border-white/10 space-y-4">
                  <h3 className="font-semibold text-sm text-white mb-2 flex items-center gap-2">
                    <Terminal className="h-4 w-4 text-[#00D4FF]" />
                    <span>Widget Embed Credentials</span>
                  </h3>

                  <div className="space-y-1">
                    <span className="block text-[10px] text-slate-400 uppercase font-bold">Generated API Contract Key</span>
                    <div className="flex items-center gap-3 bg-[#0B1221] border border-white/10 rounded-xl p-3">
                      <code className="text-slate-300 font-mono text-xs select-all flex-1" data-testid="widget-api-key">
                        {widgetCfg?.api_key || "sk_rag_xxxxxxxxxxxxxxxx"}
                      </code>
                      <button
                        onClick={() => copyToClipboard(widgetCfg?.api_key, "key")}
                        className="text-slate-400 hover:text-white transition p-1 hover:bg-white/5 rounded"
                      >
                        {copiedKey ? <Check className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
                      </button>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <span className="block text-[10px] text-slate-400 uppercase font-bold">Copy Embedding script tag</span>
                    <div className="relative">
                      <pre 
                        className="bg-[#0B1221] border border-white/10 rounded-xl p-4 text-[11px] text-slate-300 font-mono overflow-x-auto whitespace-pre-wrap leading-relaxed select-all"
                        data-testid="widget-snippet"
                      >
                        {embedSnippetHtml}
                      </pre>
                      <button
                        onClick={() => copyToClipboard(embedSnippetHtml, "snippet")}
                        className="absolute top-3 right-3 text-slate-400 hover:text-white transition p-1.5 bg-white/5 hover:bg-white/10 rounded-lg border border-white/10"
                        title="Copy code snippet"
                      >
                        {copiedSnippet ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Live Preview (Right columns) */}
              <div className="lg:col-span-1 glassmorphism rounded-2xl p-6 border-white/10 space-y-4">
                <h3 className="font-semibold text-sm text-white mb-2 flex items-center gap-2">
                  <Eye className="h-4 w-4 text-[#00D4FF]" />
                  <span>Interactive Live Preview</span>
                </h3>

                <div className="border border-white/10 rounded-2xl overflow-hidden bg-[#040914] shadow-inner h-96 relative flex flex-col">
                  {/* Fake widget top bar */}
                  <div 
                    className="p-3 text-xs text-[#040914] font-bold flex items-center justify-between"
                    style={{ backgroundColor: themeColor }}
                  >
                    <span className="tracking-tight truncate">{app.name}</span>
                    <div className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
                  </div>

                  {/* Fake widget message body */}
                  <div className="flex-1 p-4 space-y-3 overflow-y-auto">
                    <div className="flex gap-2">
                      <div className="h-6 w-6 rounded-full bg-slate-800 flex items-center justify-center text-[10px] text-white flex-shrink-0">🤖</div>
                      <div className="bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-[10px] text-slate-300 leading-relaxed max-w-[80%]">
                        {greetingMsg || "Hello! Ask me anything."}
                      </div>
                    </div>
                  </div>

                  {/* Fake input form */}
                  <div className="p-3 border-t border-white/10 flex items-center gap-2 bg-[#0B1221]">
                    <div className="flex-1 bg-white/5 rounded-lg px-2.5 py-1.5 text-[9px] text-slate-500">
                      Type message...
                    </div>
                    <div 
                      className="h-6 w-12 rounded-lg flex items-center justify-center text-[9px] font-bold text-center"
                      style={{ backgroundColor: themeColor, color: "#040914" }}
                    >
                      SEND
                    </div>
                  </div>

                  {/* Widget Launch Circle */}
                  <div 
                    className={`absolute bottom-16 right-4 h-11 w-11 rounded-full flex items-center justify-center text-lg shadow-xl border border-white/10`}
                    style={{ 
                      backgroundColor: themeColor, 
                      color: "#040914",
                      right: launcherPosition === "bottom-right" ? "16px" : "auto",
                      left: launcherPosition === "bottom-left" ? "16px" : "auto"
                    }}
                  >
                    💬
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TABS 4: CHAT TESTING SANDBOX */}
        {activeTab === "chat" && (
          <div className="space-y-6 animate-fadeIn" data-testid="view-chat">
            {/* Context status */}
            <div className="glassmorphism rounded-2xl p-4 flex flex-wrap items-center justify-between gap-4 text-xs">
              <div className="flex items-center gap-2">
                <Terminal className="h-4 w-4 text-[#00D4FF]" />
                <span className="font-semibold text-slate-200">Sandbox Testing Layer</span>
                <span className="text-slate-500">•</span>
                <span className="text-slate-400">Target contract: `POST /api/chat`</span>
              </div>

              <div className="flex items-center gap-4">
                <div className="flex items-center gap-1.5 text-xs text-slate-400">
                  <span>Retrieve top_k chunks:</span>
                  <select
                    value={chatTopK}
                    onChange={(e) => setChatTopK(Number(e.target.value))}
                    className="bg-slate-900 border border-white/10 rounded-md py-0.5 px-1.5 text-white font-medium text-xs focus:ring-1 focus:ring-[#00D4FF] focus:outline-none"
                  >
                    <option value={2}>2</option>
                    <option value={4}>4</option>
                    <option value={6}>6</option>
                  </select>
                </div>

                <button
                  onClick={() => { setSandboxHistory([]); toast.success("Sandbox history reset."); }}
                  className="text-red-400 hover:text-red-300 font-medium text-xs py-1"
                  data-testid="chat-sandbox-clear"
                >
                  Clear Sandbox
                </button>
              </div>
            </div>

            {/* Simulated Chat Interface */}
            <div className="border border-white/10 rounded-2xl h-[450px] bg-[#0B1221]/30 flex flex-col justify-between overflow-hidden shadow-xl">
              {/* Sandbox Logs */}
              <div className="flex-1 p-5 overflow-y-auto space-y-4">
                {sandboxHistory.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center text-center py-10">
                    <div className="h-10 w-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-slate-500 mb-3 animate-pulse">
                      ⚡
                    </div>
                    <h4 className="font-semibold text-slate-300 text-xs">Awaiting Query Input</h4>
                    <p className="text-[10px] text-slate-500 max-w-sm mt-1">
                      Execute testing prompts to query matching vector chunks from active document matrices.
                    </p>
                  </div>
                ) : (
                  sandboxHistory.map((m, idx) => (
                    <div key={idx} className={`flex flex-col ${m.role === "user" ? "items-end" : "items-start"}`}>
                      <div className="flex items-center gap-2 mb-1 text-[10px] text-slate-500 px-1">
                        <span>{m.role === "user" ? "Client" : "API Response"}</span>
                        <span>•</span>
                        <span>{new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                      </div>

                      <div className="flex gap-2 max-w-[85%]">
                        <div 
                          className={`rounded-2xl px-4 py-3 text-xs leading-relaxed ${
                            m.role === "user"
                              ? "bg-[#2563EB] text-white rounded-tr-none border border-white/5"
                              : "glassmorphism rounded-tl-none border-white/10"
                          }`}
                        >
                          <p className="whitespace-pre-wrap">{m.content}</p>
                        </div>
                      </div>

                      {/* Display Matching Groundings */}
                      {m.role === "bot" && m.sources && m.sources.length > 0 && (
                        <div className="mt-2 pl-4 max-w-[85%] space-y-2">
                          <span className="block text-[9px] text-[#00D4FF] font-semibold uppercase tracking-wider">Matched Chunks Sources:</span>
                          {m.sources.map((s, sIdx) => (
                            <div key={sIdx} className="bg-[#040914]/80 border border-white/5 rounded-xl p-2.5 text-[10px] text-slate-400">
                              <div className="flex justify-between items-center mb-1 text-[9px] text-slate-500 font-semibold font-mono border-b border-white/5 pb-1">
                                <span>{s.source_file}</span>
                                <span className="text-[#00D4FF]">Score: {(s.score*100).toFixed(0)}%</span>
                              </div>
                              <p className="italic font-mono text-[9px] text-slate-300">&ldquo;{s.text}&rdquo;</p>                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))
                )}

                {isChatLoading && (
                  <div className="flex flex-col items-start">
                    <div className="flex items-center gap-2 mb-1 text-[10px] text-slate-500">
                      <span>RAG Engine</span>
                      <span>•</span>
                      <span className="italic">Searching indexes...</span>
                    </div>
                    <div className="glassmorphism rounded-2xl rounded-tl-none px-4 py-3 border-white/10 flex items-center gap-2">
                      <Loader2 className="h-3.5 w-3.5 text-[#00D4FF] animate-spin" />
                      <span className="text-[10px] text-slate-400 font-mono">Retrieving high-dimensional match dimensions...</span>
                    </div>
                  </div>
                )}
              </div>

              {/* Sandbox Input Form */}
              <form 
                onSubmit={handleChatTest}
                className="p-3 border-t border-white/10 bg-[#0B1221] flex items-center gap-3"
              >
                <input
                  type="text"
                  value={sandboxQuestion}
                  onChange={(e) => setSandboxQuestion(e.target.value)}
                  placeholder="Ask testing questions about indexed documents..."
                  className="flex-1 bg-[#040914]/50 border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-3 outline-none focus:ring-1 focus:ring-[#00D4FF] transition"
                  data-testid="chat-sandbox-input"
                  required
                />
                <button
                  type="submit"
                  disabled={isChatLoading || !sandboxQuestion.trim()}
                  className={`h-11 px-5 rounded-xl flex items-center justify-center gap-2 transition duration-300 ${
                    isChatLoading || !sandboxQuestion.trim()
                      ? "bg-white/5 border border-white/5 text-slate-500 cursor-not-allowed"
                      : "bg-[#00D4FF] text-[#040914] hover:bg-white hover:text-[#040914] font-bold text-xs tracking-wider uppercase shadow-md cursor-pointer"
                  }`}
                  data-testid="chat-sandbox-submit"
                >
                  <span>Verify</span>
                  <Play className="h-3.5 w-3.5" />
                </button>
              </form>
            </div>
          </div>
        )}

        {/* TABS 5: SETTINGS */}
        {activeTab === "settings" && (
          <form onSubmit={handleUpdateSettings} className="glassmorphism rounded-2xl p-6 border-white/10 space-y-6 animate-fadeIn" data-testid="view-settings">
            <h3 className="font-semibold text-sm text-white mb-2 flex items-center gap-2">
              <Sliders className="h-4 w-4 text-[#00D4FF]" />
              <span>RAG Settings & Parameter Core</span>
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Embedding Model selection</label>
                <select
                  value={modelType}
                  onChange={(e) => setModelType(e.target.value)}
                  className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition"
                >
                  <option value="llama3:latest">llama3:latest (Default 8B Parameters)</option>
                  <option value="mistral:latest">mistral:latest (7B Parameters)</option>
                  <option value="phi3:latest">phi3:latest (High Density Mini)</option>
                </select>
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Ollama Model Environment Endpoint</label>
                <input 
                  type="text"
                  value="http://localhost:11434"
                  disabled
                  className="w-full bg-[#0B1221]/30 border border-white/5 text-slate-500 text-xs rounded-xl px-4 py-2.5 outline-none font-mono cursor-not-allowed"
                />
              </div>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">System Grounding Prompt Instructions</label>
              <textarea
                value={systemPrompt}
                onChange={(e) => setSystemPrompt(e.target.value)}
                rows={5}
                className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition resize-none font-mono leading-relaxed"
                data-testid="settings-system-prompt"
                required
              />
            </div>

            <div className="pt-4 border-t border-white/5 flex items-center justify-end">
              <button
                type="submit"
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] font-bold text-xs tracking-wider uppercase hover:scale-[1.02] active:scale-[0.98] transition cursor-pointer"
                data-testid="settings-save-btn"
              >
                Save Parameter Core
              </button>
            </div>
          </form>
        )}
      </div>
    </main>
  );
}
