import React from "react";
import '../output.css'
const QueryResponse = ({ response }) => {
  return (
    response && (
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg mt-4 text-white">
        <h2 className="text-xl font-bold text-blue-400">Query Response</h2>
        <pre className="bg-gray-900 p-4 rounded-md overflow-auto whitespace-pre-wrap border border-gray-700 text-green-400">
          {response.output || "No output available"}
        </pre>
      </div>
    )
  );
};

export default QueryResponse;
