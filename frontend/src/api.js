// src/api.js
export const API_BASE = "http://localhost:8000";

export async function fetchEmails() {
  const res = await fetch(`${API_BASE}/gmail/emails`);
  if (!res.ok) throw new Error("Failed to load emails");
  return res.json(); // { emails: [...] }
}

export async function trustSender(sender) {
  const res = await fetch(`${API_BASE}/gmail/action`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sender, action: "trust" }),
  });
  if (!res.ok) throw new Error("Failed to trust sender");
  return res.json();
}

export async function suspendSender(sender) {
  const res = await fetch(`${API_BASE}/gmail/action`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sender, action: "suspend" }),
  });
  if (!res.ok) throw new Error("Failed to suspend sender");
  return res.json();
}
