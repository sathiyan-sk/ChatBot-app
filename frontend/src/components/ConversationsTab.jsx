import { useState, useEffect } from "react";
import { apiClient } from "@/api/client";
import { ArrowLeft, MessageSquare, Loader2 } from "lucide-react";
import { toast } from "sonner";

export default function ConversationsTab({ applicationId }) {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [conversationMessages, setConversationMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isDetailLoading, setIsDetailLoading] = useState(false);

  const loadConversations = async () => {
    setIsLoading(true);
    try {
      const res = await apiClient.get(`/admin/conversations/application/${applicationId}`);
      setConversations(res.data);
    } catch (e) {
      console.error(e);
      toast.error("Failed to load conversations.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let isMounted = true;

    const fetchConversations = async () => {
      try {
        const res = await apiClient.get(`/admin/conversations/application/${applicationId}`);
        if (isMounted) setConversations(res.data);
      } catch (e) {
        console.error(e);
        if (isMounted) toast.error("Failed to load conversations.");
      }
    };

    fetchConversations();

    return () => {
      isMounted = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [applicationId]);

  const openConversation = async (convId) => {
    setIsDetailLoading(true);
    try {
      const res = await apiClient.get(`/admin/conversations/${convId}`);
      setSelectedConversation(res.data.conversation);
      setConversationMessages(res.data.messages || []);
    } catch (e) {
      console.error(e);
      toast.error("Failed to load conversation detail.");
    } finally {
      setIsDetailLoading(false);
    }
  };

  const closeConversation = async (convId) => {
    try {
      await apiClient.delete(`/admin/conversations/${convId}`);
      toast.success("Conversation closed.");
      setSelectedConversation(null);
      setConversationMessages([]);
      loadConversations();
    } catch (e) {
      console.error(e);
      toast.error("Failed to close conversation.");
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn" data-testid="view-conversations">
      <div className="glassmorphism rounded-2xl p-6 border-white/10">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-semibold text-sm text-white flex items-center gap-2">
              <MessageSquare className="h-4 w-4 text-[#00D4FF]" />
              <span>Conversation History</span>
            </h3>
            <p className="text-slate-400 text-xs mt-0.5">Browse and debug conversations for this application.</p>
          </div>
          <button
            onClick={loadConversations}
            className="px-3 py-1.5 rounded-lg border border-white/10 text-slate-400 hover:text-white hover:bg-white/5 transition text-xs"
          >
            Refresh
          </button>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-6 w-6 text-[#00D4FF] animate-spin" />
          </div>
        ) : selectedConversation ? (
          <div>
            <button
              onClick={() => { setSelectedConversation(null); setConversationMessages([]); }}
              className="flex items-center gap-1.5 text-xs text-[#00D4FF] hover:text-white transition mb-4"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              <span>Back to list</span>
            </button>

            <div className="flex items-center justify-between mb-4">
              <div>
                <h4 className="font-semibold text-sm text-white">
                  {selectedConversation.title || "Untitled Conversation"}
                </h4>
                <p className="text-[10px] text-slate-500 font-mono mt-0.5">
                  ID: {selectedConversation.id} • {selectedConversation.conversation_identity}
                </p>
              </div>
              <button
                onClick={() => closeConversation(selectedConversation.id)}
                className="px-3 py-1.5 rounded-lg border border-red-500/20 text-red-400 hover:bg-red-500/10 transition text-xs"
              >
                Close Conversation
              </button>
            </div>

            {isDetailLoading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-6 w-6 text-[#00D4FF] animate-spin" />
              </div>
            ) : (
              <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2">
                {conversationMessages.length === 0 ? (
                  <p className="text-center text-slate-500 text-xs py-8">No messages in this conversation.</p>
                ) : (
                  conversationMessages.map((msg, idx) => (
                    <div key={idx} className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}>
                      <div className="flex items-center gap-2 mb-1 text-[10px] text-slate-500 px-1">
                        <span>{msg.role === "user" ? "User" : "Assistant"}</span>
                        <span>•</span>
                        <span>{new Date(msg.created_at || msg.timestamp).toLocaleString()}</span>
                      </div>
                      <div className={`rounded-xl px-4 py-2.5 text-xs leading-relaxed max-w-[85%] ${
                        msg.role === "user"
                          ? "bg-[#2563EB] text-white rounded-tr-none border border-white/5"
                          : "bg-white/5 border border-white/10 rounded-tl-none"
                      }`}>
                        {msg.content}
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        ) : conversations.length === 0 ? (
          <div className="text-center py-12">
            <MessageSquare className="h-10 w-10 text-slate-600 mx-auto mb-3" />
            <p className="text-slate-400 text-xs">No conversations found for this application.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-white/10 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
                  <th className="py-3 px-4">Title</th>
                  <th className="py-3 px-4">Identity</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Created</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {conversations.map((conv) => (
                  <tr key={conv.id} className="border-b border-white/5 hover:bg-white/2.5 transition duration-200">
                    <td className="py-3 px-4 font-semibold text-slate-200">{conv.title || "Untitled"}</td>
                    <td className="py-3 px-4 font-mono text-slate-400">{conv.conversation_identity}</td>
                    <td className="py-3 px-4">
                      {conv.is_active ? (
                        <span className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-full text-[10px] font-medium font-mono uppercase">active</span>
                      ) : (
                        <span className="bg-slate-500/10 border border-slate-500/20 text-slate-400 px-2 py-0.5 rounded-full text-[10px] font-medium font-mono uppercase">closed</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-slate-400 font-mono">{new Date(conv.created_at).toLocaleDateString()}</td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => openConversation(conv.id)}
                        className="px-3 py-1.5 rounded-lg border border-[#00D4FF]/20 text-[#00D4FF] hover:bg-[#00D4FF]/10 transition text-xs"
                        data-testid={`view-conv-${conv.id}`}
                      >
                        View
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
  );
}