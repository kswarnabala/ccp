import React from "react";
import axios from "axios";

export default function EmailView({ selected, refreshEmails, refreshSuspended }) {
  if (!selected) {
    return <div className="flex items-center justify-center h-full">Select an email to read</div>;
  }

  const markSafe = async () => {
    await axios.patch(`http://localhost:8000/emails/${selected.id}/mark-safe`);
    refreshEmails(); // reload inbox after marking safe
  };

  const suspendAccount = async () => {
    await axios.patch(`http://localhost:8000/accounts/${selected.from}/suspend`);
    refreshEmails();     // reload inbox (removes suspended emails)
    refreshSuspended();  // reload suspended accounts
  };

  return (
    <div className="p-4">
      <h2 className="text-lg font-bold">{selected.subject}</h2>
      <p className="text-sm text-gray-400">From: {selected.from}</p>
      <div className="my-4">{selected.body}</div>
      <div className="flex gap-4">
        <button onClick={markSafe} className="bg-green-600 px-4 py-2 rounded text-white">Mark Safe</button>
        <button onClick={suspendAccount} className="bg-red-600 px-4 py-2 rounded text-white">Suspend Sender</button>
      </div>
    </div>
  );
}
