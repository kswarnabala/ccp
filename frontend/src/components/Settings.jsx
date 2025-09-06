import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Settings() {
  const [darkMode, setDarkMode] = useState(false);
  const [zeroTrust, setZeroTrust] = useState(false);
  const [suspendedAccounts, setSuspendedAccounts] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/suspended-accounts")
      .then(res => setSuspendedAccounts(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow">
      <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-100">Settings</h2>
      
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-gray-800 dark:text-gray-200">Dark Mode</span>
          <input
            type="checkbox"
            checked={darkMode}
            onChange={() => setDarkMode(!darkMode)}
            className="w-5 h-5"
          />
        </div>

        <div className="flex justify-between items-center">
          <span className="text-gray-800 dark:text-gray-200">Zero Trust Mode</span>
          <input
            type="checkbox"
            checked={zeroTrust}
            onChange={() => setZeroTrust(!zeroTrust)}
            className="w-5 h-5"
          />
        </div>

        <div>
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200">Suspended Accounts</h3>
          <ul className="mt-2 space-y-2">
            {suspendedAccounts.map((acc, idx) => (
              <li key={idx} className="p-2 bg-gray-100 dark:bg-gray-700 rounded-lg">
                {acc}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
