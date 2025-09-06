import { useState, useEffect } from "react";

function Sidebar() {
  const [suspended, setSuspended] = useState({});

  useEffect(() => {
    fetch("http://127.0.0.1:8000/actions/suspended")
      .then(res => res.json())
      .then(data => setSuspended(data));
  }, []);

  return (
    <div className="sidebar">
      <h3>Inbox</h3>
      <ul>
        <li>Primary</li>
        <li>Drafts</li>
        <li>Sent</li>
      </ul>

      <h3>Suspended Accounts</h3>
      <ul>
        {Object.keys(suspended).length === 0 && <li>No suspended senders</li>}
        {Object.keys(suspended).map(sender => (
          <li key={sender}>{sender}</li>
        ))}
      </ul>
    </div>
  );
}

export default Sidebar;
