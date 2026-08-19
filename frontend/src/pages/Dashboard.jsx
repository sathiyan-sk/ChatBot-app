import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { apiClient } from "@/api/client";
import {
  Plus, Database, Loader2, Cpu, Eye, Pencil, Power,
  Copy, Check, KeyRound, AlertTriangle
} from "lucide-react";
import { toast } from "sonner";

export default function Dashboard() {
  const [apps, setApps] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Create/edit modal state
  const [showModal, setShowModal] = useState(false);
  const [editingApp, setEditingApp] = useState(null);
  const [formName, setFormName] = useState("");
  const [formDesc, setFormDesc] = useState("");
  const [formClientType, setFormClientType] = useState("website");
  const [formOrigins, setFormOrigins] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // API key reveal modal state
  const [keyModal, setKeyModal] = useState(null);
  const [copiedKey, setCopiedKey] = useState(false);

  useEffect(() => {
    let isMounted = true;

    const loadApps = async () => {
      try {
        const response = await apiClient.get("/admin/applications");
        if (isMounted) setApps(response.data);
      } catch (e) {
        if (isMounted) {
          console.error(e);
          toast.error("Failed to fetch applications from RAG backend.");
        }
      } finally {
        if (isMounted) setIsLoading(false);
      }
    };

    loadApps();

    return () => {
      isMounted = false;
    };
  }, []);

  const openCreateModal = () => {
    setEditingApp(null);
    setFormName("");
    setFormDesc("");
    setFormClientType("website");
    setFormOrigins("");
    setShowModal(true);
  };

  const openEditModal = (app) => {
    setEditingApp(app);
    setFormName(app.name);
    setFormDesc(app.description || "");
    setFormClientType(app.client_type);
    setFormOrigins((app.allowed_origins || []).join(", "));
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formName.trim() || isSubmitting) return;

    setIsSubmitting(true);
    const originsArray = formOrigins
      .split(",")
      .map((o) => o.trim())
      .filter(Boolean);

    try {
      if (editingApp) {
        // Edit path — PUT /admin/applications/{id}
        await apiClient.put(`/admin/applications/${editingApp.id}`, {
          name: formName.trim(),
          description: formDesc.trim() || null,
          client_type: formClientType,
          allowed_origins: originsArray,
          is_active: editingApp.is_active,
        });
        toast.success(`Application "${formName}" updated!`);
      } else {
        // Create path — POST /admin/applications
        const response = await apiClient.post("/admin/applications", {
          name: formName.trim(),
          description: formDesc.trim() || null,
          client_type: formClientType,
          allowed_origins: originsArray,
        });

        // Show API key ONCE with copy + warning
        setKeyModal({
          key: response.data.api_key,
          prefix: response.data.api_key_prefix,
          name: response.data.application.name,
        });
        toast.success(`Application "${formName}" created!`, {
          description: "Save your API key now — it won't be shown again.",
        });
      }

      setShowModal(false);
      // Refresh list
      const appsRes = await apiClient.get("/admin/applications");
      setApps(appsRes.data);
    } catch (e) {
      console.error(e);
      const msg = e.response?.data?.detail || "Operation failed.";
      toast.error(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeactivate = async (app) => {
    if (!window.confirm(`Deactivate "${app.name}"? The app will no longer be able to authenticate against the backend.`)) return;
    try {
      await apiClient.delete(`/admin/applications/${app.id}`);
      toast.success(`Application "${app.name}" deactivated.`);
      // Refresh list
      const appsRes = await apiClient.get("/admin/applications");
      setApps(appsRes.data);
    } catch (e) {
      console.error(e);
      toast.error("Failed to deactivate application.");
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(true);
    setTimeout(() => setCopiedKey(false), 2000);
    toast.success("API key copied!");
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
            Register namespaces, provision embeddable chat widgets, and synchronize document indices within isolated application contexts.
          </p>
        </div>

        <button
          onClick={openCreateModal}
          className="flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] font-semibold text-xs tracking-wider uppercase hover:scale-[1.03] active:scale-[0.97] transition duration-300 shadow-[0_0_15px_rgba(0,212,255,0.2)] cursor-pointer"
          data-testid="create-app-trigger"
        >
          <Plus className="h-4 w-4" />
          <span>Create Application</span>
        </button>
      </div>

      {/* Loading */}
      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="h-8 w-8 text-[#00D4FF] animate-spin" />
        </div>
      ) : apps.length === 0 ? (
        /* Empty state */
        <div className="text-center py-20 border border-dashed border-white/5 rounded-3xl bg-white/2">
          <Database className="h-12 w-12 text-slate-600 mx-auto mb-4" />
          <h3 className="font-semibold text-base text-slate-300">No applications found</h3>
          <p className="text-slate-500 text-xs mt-1.5 max-w-md mx-auto leading-relaxed">
            Create an isolated namespace to begin uploading documents, customizing styles, and testing Retrieval Augmented Generation parameters.
          </p>
        </div>
      ) : (
        /* Table */
        <div className="glassmorphism rounded-2xl border-white/10 overflow-hidden" data-testid="applications-table">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-white/10 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
                  <th className="py-4 px-6">Name</th>
                  <th className="py-4 px-4">Slug</th>
                  <th className="py-4 px-4">Client Type</th>
                  <th className="py-4 px-4">Status</th>
                  <th className="py-4 px-4">Created At</th>
                  <th className="py-4 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {apps.map((app) => (
                  <tr
                    key={app.id}
                    className="border-b border-white/5 hover:bg-white/2.5 transition duration-200"
                    data-testid={`app-row-${app.id}`}
                  >
                    <td className="py-4 px-6">
                      <Link
                        to={`/dashboard/${app.id}`}
                        className="flex items-center gap-3 group"
                        data-testid={`app-link-${app.id}`}
                      >
                        <div className="p-2 bg-white/5 rounded-lg border border-white/10 text-[#00D4FF] flex-shrink-0">
                          <Database className="h-4 w-4" />
                        </div>
                        <div>
                          <div className="font-semibold text-slate-200 group-hover:text-[#00D4FF] transition">
                            {app.name}
                          </div>
                          {app.description && (
                            <div className="text-[10px] text-slate-500 max-w-[240px] truncate">
                              {app.description}
                            </div>
                          )}
                        </div>
                      </Link>
                    </td>
                    <td className="py-4 px-4 font-mono text-slate-400">{app.slug}</td>
                    <td className="py-4 px-4">
                      <span className="flex items-center gap-1.5 text-slate-300">
                        <Cpu className="h-3 w-3 text-slate-400" />
                        <span className="capitalize">{app.client_type}</span>
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      {app.is_active ? (
                        <span className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-2.5 py-1 rounded-full text-[10px] font-medium font-mono uppercase">
                          active
                        </span>
                      ) : (
                        <span className="bg-red-500/10 border border-red-500/20 text-red-400 px-2.5 py-1 rounded-full text-[10px] font-medium font-mono uppercase">
                          inactive
                        </span>
                      )}
                    </td>
                    <td className="py-4 px-4 text-slate-400 font-mono">
                      {new Date(app.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center justify-end gap-1.5">
                        {/* View */}
                        <Link
                          to={`/dashboard/${app.id}`}
                          className="p-2 rounded-lg border border-white/10 text-slate-400 hover:text-[#00D4FF] hover:border-[#00D4FF]/30 hover:bg-[#00D4FF]/5 transition"
                          title="View"
                          data-testid={`view-btn-${app.id}`}
                        >
                          <Eye className="h-3.5 w-3.5" />
                        </Link>
                        {/* Edit */}
                        <button
                          onClick={() => openEditModal(app)}
                          className="p-2 rounded-lg border border-white/10 text-slate-400 hover:text-amber-400 hover:border-amber-400/30 hover:bg-amber-400/5 transition"
                          title="Edit"
                          data-testid={`edit-btn-${app.id}`}
                        >
                          <Pencil className="h-3.5 w-3.5" />
                        </button>
                        {/* Deactivate */}
                        <button
                          onClick={() => handleDeactivate(app)}
                          disabled={!app.is_active}
                          className={`p-2 rounded-lg border transition ${
                            app.is_active
                              ? "border-red-500/10 text-red-400 hover:text-red-300 hover:border-red-500/30 hover:bg-red-500/10 cursor-pointer"
                              : "border-white/5 text-slate-600 cursor-not-allowed"
                          }`}
                          title="Deactivate"
                          data-testid={`deactivate-btn-${app.id}`}
                        >
                          <Power className="h-3.5 w-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Create/Edit Modal */}
      {showModal && (
        <div
          className="fixed inset-0 z-50 bg-[#040914]/80 backdrop-blur-md flex items-center justify-center p-4 animate-fadeIn"
          data-testid="app-form-modal"
        >
          <div className="w-full max-w-md glassmorphism rounded-3xl border-white/10 p-7 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#2563EB] to-[#00D4FF]"></div>

            <h3 className="font-semibold text-lg text-white mb-1 tracking-tight">
              {editingApp ? "Edit Application" : "Create Application"}
            </h3>
            <p className="text-slate-400 text-xs mb-5">
              {editingApp
                ? `Update namespace "${editingApp.name}" configuration.`
                : "Isolated context mapping specific knowledge bases."}
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Name *
                </label>
                <input
                  type="text"
                  value={formName}
                  onChange={(e) => setFormName(e.target.value)}
                  placeholder="e.g. FAQ Support Assistant"
                  className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition"
                  required
                  data-testid="app-form-name"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Description
                </label>
                <textarea
                  value={formDesc}
                  onChange={(e) => setFormDesc(e.target.value)}
                  placeholder="Describe the application scope..."
                  rows={3}
                  className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition resize-none"
                  data-testid="app-form-desc"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Client Type *
                </label>
                <select
                  value={formClientType}
                  onChange={(e) => setFormClientType(e.target.value)}
                  className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition"
                  required
                  data-testid="app-form-client-type"
                >
                  <option value="website">Website</option>
                  <option value="mobile">Mobile App</option>
                  <option value="desktop">Desktop App</option>
                  <option value="api">API Integration</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Allowed Origins (comma-separated)
                </label>
                <input
                  type="text"
                  value={formOrigins}
                  onChange={(e) => setFormOrigins(e.target.value)}
                  placeholder="https://example.com, https://app.example.com"
                  className="w-full bg-[#0B1221] border border-white/10 focus:border-[#00D4FF] text-white text-xs rounded-xl px-4 py-2.5 outline-none focus:ring-1 focus:ring-[#00D4FF] transition"
                  data-testid="app-form-origins"
                />
                <p className="text-[10px] text-slate-500 mt-1">Leave empty to allow all origins</p>
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-white/5">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/5 transition text-xs font-semibold focus:outline-none"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting || !formName.trim()}
                  className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] font-bold text-xs tracking-wider uppercase hover:scale-[1.02] active:scale-[0.98] transition shadow-md focus:outline-none cursor-pointer"
                  data-testid="app-form-submit"
                >
                  {isSubmitting
                    ? editingApp ? "Saving..." : "Creating..."
                    : editingApp ? "Save Changes" : "Confirm Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* API Key Reveal Modal (shown once on create) */}
      {keyModal && (
        <div
          className="fixed inset-0 z-[60] bg-[#040914]/90 backdrop-blur-md flex items-center justify-center p-4 animate-fadeIn"
          data-testid="api-key-modal"
        >
          <div className="w-full max-w-md glassmorphism rounded-3xl border-amber-500/30 p-7 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-amber-500 to-[#00D4FF]"></div>

            <div className="flex items-center gap-2 mb-3">
              <div className="p-2.5 bg-amber-500/10 rounded-xl border border-amber-500/20 text-amber-400">
                <KeyRound className="h-5 w-5" />
              </div>
              <div>
                <h3 className="font-semibold text-lg text-white tracking-tight">
                  API Key Generated
                </h3>
                <p className="text-[10px] text-slate-400">
                  For application: <span className="text-[#00D4FF] font-mono">{keyModal.name}</span>
                </p>
              </div>
            </div>

            {/* Warning banner */}
            <div className="flex items-start gap-2.5 p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl mb-4">
              <AlertTriangle className="h-4 w-4 text-amber-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-[11px] font-semibold text-amber-300">This key will NOT be shown again!</p>
                <p className="text-[10px] text-amber-400/80 mt-0.5 leading-relaxed">
                  Copy it now and store it securely. The backend only returns the full API key once at creation time.
                </p>
              </div>
            </div>

            {/* Key display + copy */}
            <div className="space-y-2">
              <span className="block text-[10px] text-slate-400 uppercase font-bold tracking-wider">Full API Key</span>
              <div className="flex items-center gap-2 bg-[#0B1221] border border-white/10 rounded-xl p-3">
                <code className="text-slate-200 font-mono text-[11px] select-all flex-1 break-all leading-relaxed" data-testid="api-key-value">
                  {keyModal.key}
                </code>
                <button
                  onClick={() => copyToClipboard(keyModal.key)}
                  className="shrink-0 p-2 rounded-lg border border-white/10 text-slate-300 hover:text-[#00D4FF] hover:border-[#00D4FF]/30 transition"
                  title="Copy API key"
                  data-testid="api-key-copy-btn"
                >
                  {copiedKey ? <Check className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
                </button>
              </div>

              <div className="pt-2">
                <span className="block text-[10px] text-slate-500 uppercase font-bold tracking-wider">Key Prefix</span>
                <code className="text-slate-300 font-mono text-[11px]">{keyModal.prefix}</code>
              </div>
            </div>

            <button
              onClick={() => setKeyModal(null)}
              className="mt-5 w-full h-11 bg-gradient-to-r from-[#2563EB] to-[#00D4FF] text-[#040914] font-bold text-xs tracking-widest uppercase rounded-xl transition duration-300 hover:scale-[1.01] active:scale-[0.99] shadow-[0_0_15px_rgba(0,212,255,0.2)] cursor-pointer"
              data-testid="api-key-close-btn"
            >
              I've Saved My Key
            </button>
          </div>
        </div>
      )}
    </main>
  );
}