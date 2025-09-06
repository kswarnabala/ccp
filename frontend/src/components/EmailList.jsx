import React, { useEffect, useState } from "react";

const EmailList = ({ view }) => {
  const [emails, setEmails] = useState([]);

  // Fetch emails depending on view (inbox or suspended)
  const fetchEmails = async () => {
    try {
      const url =
        view === "suspended"
          ? "http://127.0.0.1:8000/gmail/suspended"
          : "http://127.0.0.1:8000/gmail/emails";

      const res = await fetch(url);
      const json = await res.json();
      setEmails(json.emails || []);
    } catch (err) {
      console.error("Failed to fetch emails:", err);
    }
  };

  useEffect(() => {
    fetchEmails();
  }, [view]);

  const handleAction = async (emailId, action) => {
    try {
      await fetch("http://127.0.0.1:8000/gmail/action", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_id: emailId, action }),
      });
      fetchEmails(); // refresh after action
    } catch (err) {
      console.error("Action failed:", err);
    }
  };

  return (
    <div className="p-6 text-white">
      <h2 className="text-xl font-bold mb-4">
        {view === "suspended" ? "Suspended Accounts" : "Inbox"}
      </h2>
      <div className="space-y-4">
        {emails.map((email) => (
          <div
            key={email.id}
            className="bg-gray-800 p-4 rounded-lg shadow-md"
          >
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-lg font-semibold">{email.subject}</h3>
              <span
                className={`px-2 py-1 rounded-md text-xs font-semibold ${
                  email.classification === "Safe"
                    ? "bg-green-600"
                    : "bg-red-600"
                }`}
              >
                {email.classification}
              </span>
            </div>
            <p className="text-sm text-gray-300 mb-3">{email.snippet}</p>

            {view !== "suspended" && (
              <div className="flex gap-2">
                <button
                  onClick={() => handleAction(email.id, "safe")}
                  className="px-3 py-1 bg-green-700 rounded-lg hover:bg-green-800"
                >
                  Mark Safe
                </button>
                <button
                  onClick={() => handleAction(email.id, "suspend")}
                  className="px-3 py-1 bg-red-700 rounded-lg hover:bg-red-800"
                >
                  Suspend
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default EmailList;
