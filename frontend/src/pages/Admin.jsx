import React, { useState, useEffect } from "react";
import axios from "axios";
import { UploadCloud, Layers, Trash2, RefreshCw, CheckCircle2, AlertCircle, FileText, Loader2, Database } from "lucide-react";
import { toast } from "sonner";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8001";
const API = `${BACKEND_URL}/api`;

export default function Admin() {
  const [documents, setDocuments] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isRebuilding, setIsRebuilding] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [stats, setStats] = useState({ total: 0, indexed: 0, parsing: 0, uploaded: 0 });

  // Load documents
  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${API}/documents`);
      setDocuments(response.data);
    } catch (e) {
      console.error(e);
      toast.error("Failed to load document directory from server.");
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  // Compute stat widgets
  useEffect(() => {
    const total = documents.length;
    const indexed = documents.filter((d) => d.status === "indexed").length;
    const parsing = documents.filter((d) => d.status === "parsing" || d.status === "uploaded").length;
    const uploaded = documents.filter((d) => d.status === "uploaded").length;
    setStats({ total, indexed, parsing, uploaded });
  }, [documents]);

  // Status auto-polling loop (polls if any file is uploaded or parsing)
  useEffect(() => {
    const hasUnfinishedDocs = documents.some(
      (d) => d.status === "uploaded" || d.status === "parsing"
    );

    if (hasUnfinishedDocs) {
      const interval = setInterval(() => {
        fetchDocuments();
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [documents]);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      await uploadFile(files[0]);
    }
  };

  const handleFileSelect = async (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      await uploadFile(files[0]);
    }
  };

  const uploadFile = async (file) => {
    const allowedExtensions = [".pdf", ".txt", ".docx", ".csv", ".json", ".md"];
    const fileExtension = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
      toast.error(`Unsupported format. Supported: ${allowedExtensions.join(", ")}`);
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API}/documents/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      toast.success(`"${file.name}" uploaded successfully! Real-time parsing started.`);
      fetchDocuments();
    } catch (e) {
      console.error(e);
      const msg = e.response?.data?.detail || "Upload operation failed.";
      toast.error(msg);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to delete and un-index "${name}"?`)) return;

    try {
      await axios.delete(`${API}/documents/${id}`);
      toast.success(`Removed "${name}" from knowledge base.`);
      fetchDocuments();
    } catch (e) {
      console.error(e);
      toast.error("Failed to delete document.");
    }
  };

  const handleReindex = async () => {
    setIsRebuilding(true);
    try {
      const response = await axios.post(`${API}/indexing/rebuild`);
      const data = response.data;
      toast.success(
        `FAISS Index Rebuilt Successfully! Indexed ${data.document_count} documents into ${data.vector_count} dense vectors.`
      );
      fetchDocuments();
    } catch (e) {
      console.error(e);
      toast.error("FAISS Index rebuild failed.");
    } finally {
      setIsRebuilding(false);
    }
  };

  return (
    <main className="flex-1 w-full max-w-6xl mx-auto px-4 md:px-8 py-8">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
        <div>
          <h1 className="text-3xl md:text-4xl font-semibold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            Admin Knowledge Console
          </h1>
          <p className="text-slate-400 text-sm mt-1.5 leading-relaxed max-w-xl">
            Manage your vector search directory, upload PDF guidelines, monitor real-time embedding pipelines, and rebuild your FAISS index caches.
          </p>
        </div>

        {/* Global Reindex Action */}
        <button
          onClick={handleReindex}
          disabled={isRebuilding || documents.length === 0}
          className={`flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-xl font-semibold text-xs tracking-wider uppercase transition duration-300 ${
            isRebuilding || documents.length === 0
              ? "bg-white/5 border border-white/5 text-slate-400 cursor-not-allowed"
              : "bg-gradient-to-r from-[#00D4FF] to-[#2563EB] text-[#040914] hover:bg-white hover:from-white hover:to-white hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(0,212,255,0.25)]"
          }`}
          data-testid="reindex-btn"
        >
          {isRebuilding ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Rebuilding Index...</span>
            </>
          ) : (
            <>
              <RefreshCw className="h-4 w-4" />
              <span>Trigger Global Reindex</span>
            </>
          )}
        </button>
      </div>

      {/* High Density Grid Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="glassmorphism rounded-2xl p-5" data-testid="total-documents-widget">
          <div className="text-slate-400 text-[10px] md:text-xs font-semibold tracking-wider uppercase">Total Documents</div>
          <div className="text-2xl md:text-3xl font-bold text-white mt-1.5">{stats.total}</div>
        </div>
        <div className="glassmorphism rounded-2xl p-5" data-testid="indexed-documents-widget">
          <div className="text-emerald-400 text-[10px] md:text-xs font-semibold tracking-wider uppercase">Indexed Chunks</div>
          <div className="text-2xl md:text-3xl font-bold text-emerald-400 mt-1.5">{stats.indexed}</div>
        </div>
        <div className="glassmorphism rounded-2xl p-5" data-testid="parsing-documents-widget">
          <div className="text-amber-400 text-[10px] md:text-xs font-semibold tracking-wider uppercase">Parsing Pipeline</div>
          <div className="text-2xl md:text-3xl font-bold text-amber-400 mt-1.5">{stats.parsing}</div>
        </div>
        <div className="glassmorphism rounded-2xl p-5">
          <div className="text-[#00D4FF] text-[10px] md:text-xs font-semibold tracking-wider uppercase">Ollama Model</div>
          <div className="text-xs md:text-sm font-bold text-[#00D4FF] mt-3 truncate font-mono">llama3:latest</div>
        </div>
      </div>

      {/* Main Grid Content - Upload Area vs Document List Table */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        {/* Drag and Drop Zone (Left column) */}
        <div className="lg:col-span-1">
          <div className="glassmorphism rounded-2xl p-6 border-white/10 flex flex-col">
            <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center gap-2">
              <Database className="h-4 w-4 text-[#00D4FF]" />
              <span>Ingestion Pipeline</span>
            </h3>

            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => document.getElementById("admin-file-picker").click()}
              className={`border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition-all duration-300 ${
                isDragging
                  ? "border-[#00D4FF] bg-[#00D4FF]/5 scale-102"
                  : "border-white/10 hover:border-white/20 hover:bg-white/5"
              }`}
              data-testid="file-upload-zone"
            >
              <input
                id="admin-file-picker"
                type="file"
                onChange={handleFileSelect}
                className="hidden"
                accept=".pdf,.txt,.docx,.csv,.json,.md"
                data-testid="file-upload-input"
              />

              {isUploading ? (
                <div className="space-y-4">
                  <Loader2 className="h-10 w-10 text-[#00D4FF] animate-spin mx-auto" />
                  <div>
                    <p className="text-xs text-slate-200 font-semibold font-mono animate-pulse">
                      UPLOADING RAW BYTES...
                    </p>
                    <p className="text-[10px] text-slate-400 mt-1">
                      Updating knowledge store
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="p-3 bg-white/5 rounded-full border border-white/10 inline-block">
                    <UploadCloud className="h-6 w-6 text-[#00D4FF]" />
                  </div>
                  <div>
                    <p className="text-xs text-slate-200 font-semibold">
                      Drag & Drop File Here
                    </p>
                    <p className="text-[10px] text-slate-400 mt-1 leading-relaxed">
                      Or click to browse file system.<br />
                      PDF, TXT, DOCX, CSV, MD or JSON.
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Hint Widget */}
            <div className="mt-5 p-4 bg-blue-500/5 border border-blue-500/10 rounded-xl flex gap-3 text-[11px] text-slate-400 leading-relaxed">
              <AlertCircle className="h-4 w-4 text-[#00D4FF] flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold text-slate-300">Automatic Pipeline</span>: Uploaded files undergo real-time parsing, sentence splitting, and high-dimensional vector embeddings before FAISS sync.
              </div>
            </div>
          </div>
        </div>

        {/* Directory Listing (Right columns) */}
        <div className="lg:col-span-2">
          <div className="glassmorphism rounded-2xl p-6 border-white/10">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-sm text-slate-200 flex items-center gap-2">
                <Layers className="h-4 w-4 text-[#00D4FF]" />
                <span>Knowledge Directory ({documents.length})</span>
              </h3>
              {documents.some((d) => d.status === "uploaded" || d.status === "parsing") && (
                <span className="text-[10px] text-amber-400 animate-pulse font-medium font-mono flex items-center gap-1.5 bg-amber-500/5 px-2.5 py-1 rounded-full border border-amber-500/10">
                  <span className="h-1.5 w-1.5 rounded-full bg-amber-400 animate-ping"></span>
                  Processing Ingestion...
                </span>
              )}
            </div>

            {documents.length === 0 ? (
              <div className="text-center py-12 border border-dashed border-white/5 rounded-2xl">
                <FileText className="h-10 w-10 text-slate-600 mx-auto mb-3" />
                <p className="text-slate-400 text-xs">No documents uploaded yet.</p>
                <p className="text-[10px] text-slate-500 mt-1">Upload files on the left to start building your local knowledge-base.</p>
              </div>
            ) : (
              <div className="overflow-x-auto" data-testid="document-table">
                <table className="w-full text-left border-collapse text-xs">
                  <thead>
                    <tr className="border-b border-white/10 text-slate-400 font-semibold">
                      <th className="py-3 px-4">Document Details</th>
                      <th className="py-3 px-4">Size (KB)</th>
                      <th className="py-3 px-4">Pipeline Status</th>
                      <th className="py-3 px-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {documents.map((doc) => (
                      <tr 
                        key={doc.document_id}
                        className="border-b border-white/5 hover:bg-white/2.5 transition duration-200 align-middle"
                        data-testid={`document-row-${doc.document_id}`}
                      >
                        <td className="py-3.5 px-4">
                          <div className="flex items-center gap-3">
                            <div className="p-2 bg-[#0B1221] rounded-lg border border-white/5 text-[#00D4FF]">
                              <FileText className="h-4 w-4" />
                            </div>
                            <div className="max-w-[180px] md:max-w-[260px]">
                              <div className="font-semibold text-slate-100 truncate" title={doc.original_filename}>
                                {doc.original_filename}
                              </div>
                              <div className="text-[9px] text-slate-500 font-mono mt-0.5 truncate">
                                ID: {doc.document_id}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="py-3.5 px-4 text-slate-300 font-mono">
                          {doc.file_size_kb || "N/A"} KB
                        </td>
                        <td className="py-3.5 px-4" data-testid={`document-status-${doc.document_id}`}>
                          {doc.status === "indexed" && (
                            <span className="inline-flex items-center gap-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-full text-[10px] font-medium uppercase font-mono">
                              <CheckCircle2 className="h-3 w-3" />
                              <span>indexed</span>
                            </span>
                          )}
                          {doc.status === "parsing" && (
                            <span className="inline-flex items-center gap-1 bg-amber-500/10 border border-amber-500/20 text-amber-400 px-2 py-0.5 rounded-full text-[10px] font-medium uppercase font-mono">
                              <Loader2 className="h-3 w-3 animate-spin" />
                              <span>parsing...</span>
                            </span>
                          )}
                          {doc.status === "uploaded" && (
                            <span className="inline-flex items-center gap-1 bg-blue-500/10 border border-blue-500/20 text-blue-400 px-2 py-0.5 rounded-full text-[10px] font-medium uppercase font-mono">
                              <Loader2 className="h-3 w-3 animate-spin" />
                              <span>uploaded</span>
                            </span>
                          )}
                          {doc.status === "failed" && (
                            <span 
                              className="inline-flex items-center gap-1 bg-red-500/10 border border-red-500/20 text-red-400 px-2 py-0.5 rounded-full text-[10px] font-medium uppercase font-mono cursor-pointer"
                              title={doc.error_message || "Ingestion error"}
                            >
                              <AlertCircle className="h-3 w-3" />
                              <span>failed</span>
                            </span>
                          )}
                        </td>
                        <td className="py-3.5 px-4 text-right">
                          <button
                            onClick={() => handleDelete(doc.document_id, doc.original_filename)}
                            className="p-1.5 rounded-lg border border-red-500/10 hover:border-red-500/30 text-red-400 hover:bg-red-500/10 hover:text-red-300 transition duration-200 focus:outline-none"
                            title="Delete file"
                            data-testid={`delete-btn-${doc.document_id}`}
                          >
                            <Trash2 className="h-4 w-4" />
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
    </main>
  );
}
