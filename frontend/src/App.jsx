import { useEffect, useState } from "react";
import { Mail, Send, Trash2, Star, Archive, Settings } from "lucide-react";

export default function App() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);

  async function fetchEmails() {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/gmail/emails");
      const json = await res.json();
      setEmails(json.emails || []);
    } catch (e) {
      console.error(e);
      setEmails([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchEmails();
    const interval = setInterval(fetchEmails, 30_000); // refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const handleAction = async (sender, action) => {
    await fetch("http://127.0.0.1:8000/gmail/action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender, action }),
    });
    fetchEmails();
  };

  return (
    <div className="flex h-screen bg-[#0d0d0d] text-gray-200">
      {/* Sidebar */}
      <div className="w-16 md:w-60 bg-[#1a1a1a] border-r border-gray-800 flex flex-col">
        <div className="p-4 text-lg font-bold hidden md:block">ZeroTrust-AI</div>
        <ul className="flex-1 space-y-2 px-2 md:px-4">
          <li className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-[#2a2a2a] cursor-pointer">
            <Mail size={18} /> <span className="hidden md:inline">Inbox</span>
          </li>
          {/* Other menu items are just placeholders */}
          <li className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-[#2a2a2a] cursor-pointer">
            <Send size={18} /> <span className="hidden md:inline">Sent</span>
          </li>
          <li className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-[#2a2a2a] cursor-pointer">
            <Star size={18} /> <span className="hidden md:inline">Starred</span>
          </li>
          <li className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-[#2a2a2a] cursor-pointer">
            <Archive size={18} /> <span className="hidden md:inline">Archived</span>
          </li>
          <li className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-[#2a2a2a] cursor-pointer">
            <Trash2 size={18} /> <span className="hidden md:inline">Trash</span>
          </li>
        </ul>
        <div className="p-4 border-t border-gray-800">
          <button className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-[#2a2a2a] w-full">
            <Settings size={18} /> <span className="hidden md:inline">Settings</span>
          </button>
        </div>
      </div>

      {/* Email List */}
      <div className="w-1/3 border-r border-gray-800 bg-[#141414] overflow-y-auto">
        {loading && <div className="p-4">Loading emails...</div>}
        {!loading && emails.length === 0 && <div className="p-4">No emails found</div>}
        {emails.map((email) => (
          <div
            key={email.id}
            onClick={() => setSelected(email)}
            className={`px-4 py-3 border-b border-gray-800 cursor-pointer hover:bg-[#222222] ${
              selected?.id === email.id ? "bg-[#1f1f1f]" : ""
            }`}
          >
            <div className="flex justify-between items-center">
              <span className="font-semibold text-gray-100">{email.sender}</span>
              {/* Classification Badge */}
              <span
                className={`px-2 py-1 rounded-md text-xs font-semibold ${
                  email.classification === "Safe"
                    ? "bg-green-600 text-white"
                    : "bg-red-600 text-white"
                }`}
              >
                {email.classification}
              </span>
            </div>
            <p className="text-sm text-gray-300 truncate">{email.subject}</p>
          </div>
        ))}
      </div>

      {/* Email View */}
      <div className="flex-1 bg-[#121212] overflow-y-auto">
        {selected ? (
          <div className="p-6">
            <h1 className="text-xl font-bold text-white mb-2">
              {selected.subject || "(no subject)"}
            </h1>
            <p className="text-sm text-gray-400 mb-6">
              From: {selected.sender} • {selected.time}
            </p>

            {/* Action Buttons */}
            <div className="flex gap-4 mb-6">
              <button
                className="px-4 py-2 rounded-lg bg-green-600 hover:bg-green-700 text-white shadow"
                onClick={() => handleAction(selected.sender, "safe")}
              >
                Mark Safe
              </button>
              <button
                className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-white shadow"
                onClick={() => handleAction(selected.sender, "suspend")}
              >
                Suspend Sender
              </button>
            </div>

            {/* Email Body */}
            <div className="text-gray-300 leading-relaxed whitespace-pre-line">
              {selected.body || selected.snippet || "(no body)"}
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-500">
            Select an email to read
          </div>
        )}
      </div>
    </div>
  );
}
