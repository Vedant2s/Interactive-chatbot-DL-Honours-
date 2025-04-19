import React from "react";
import '../output.css'

const CommandButtons = ({ onInstall, onPopulate }) => {
  return (
    <div className="flex flex-col items-center space-y-4 mt-4">
      <button
        onClick={onInstall}
        className="bg-blue-500 text-white px-6 py-2 rounded-lg shadow-lg hover:bg-blue-600 transition duration-300  max-w-xs"
      >
        🚀 Install Requirements
      </button>
      <button
        onClick={onPopulate}
        className="bg-green-500 text-white px-6 py-2 rounded-lg shadow-lg hover:bg-green-600 transition duration-300  max-w-xs"
      >
        📊 Populate Database
      </button>
    </div>
  );
};

export default CommandButtons;
