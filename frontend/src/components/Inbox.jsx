import React, { useState } from "react";
import EmailList from "./EmailList";
import EmailView from "./EmailView";

// Dummy emails (replace with Gmail API fetch)
const initialEmails = [
  {
    id: 1,
    sender: "security@paypal.com",
    subject: "Suspicious login attempt",
    snippet: "We noticed a suspicious login attempt...",
    classification: "suspicious",
    body: "Your account has detected unusual login attempts. Click here to secure your account."
  },
  {
    id: 2,
    sender: "friend@example.com",
    subject: "Weekend plans",
    snippet: "Hey! Are you free this weekend?",
    classification: "safe",
    body: "Let’s go for a trip this weekend. What do you say?"
  }
];

const Inbox = () => {
  const [emails, setEmails] = useState(initialEmails);
  const [selectedEmail, setSelectedEmail] = useState(null);

  const handleSelectEmail = (email) => {
    setSelectedEmail(email);
  };

  const handleUpdateStatus = (id, newStatus) => {
    setEmails((prev) =>
      prev.map((email) =>
        email.id === id ? { ...email, classification: newStatus } : email
      )
    );
    if (selectedEmail) {
      setSelectedEmail({ ...selectedEmail, classification: newStatus });
    }
  };

  return (
    <div className="flex w-full h-full">
      <div className="w-1/3 border-r border-gray-200">
        <EmailList emails={emails} onSelectEmail={handleSelectEmail} />
      </div>
      <div className="w-2/3">
        {selectedEmail ? (
          <EmailView
            email={selectedEmail}
            onUpdateStatus={handleUpdateStatus}
          />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            Select an email to view
          </div>
        )}
      </div>
    </div>
  );
};

export default Inbox;
