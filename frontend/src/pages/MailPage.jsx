import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import EmailList from "../components/EmailList";

const MailPage = () => {
  const [view, setView] = useState("inbox");

  return (
    <div className="flex">
      <Sidebar setView={setView} />
      <div className="flex-1">
        <EmailList view={view} />
      </div>
    </div>
  );
};

export default MailPage;
