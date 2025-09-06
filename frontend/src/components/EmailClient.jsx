import React from "react";
import Inbox from "./Inbox";

const EmailClient = () => {
  return (
    <div className="w-full h-screen bg-gray-100 flex items-center justify-center">
      <div className="w-11/12 h-[90%] bg-white rounded-2xl shadow-lg flex overflow-hidden">
        <Inbox />
      </div>
    </div>
  );
};

export default EmailClient;
