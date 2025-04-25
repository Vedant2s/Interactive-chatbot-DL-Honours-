import React, { useState } from "react";
import FileUpload from "./pages/FileUpload";
import CommandButtons from "./pages/CommandButtons";
import QueryForm from "./pages/QueryForm";
import QueryResponse from "./pages/QueryResponse";
import "./output.css";
import ChangePrompt from "./pages/ChangePrompt";

const Home = () => {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInstallRequirements = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/run/install-requirements", {
        method: "POST",
      });
      const result = await res.json();
      alert(result.output || result.error);
    } catch (error) {
      console.error("Error installing requirements:", error);
    } finally {
      setLoading(false);
    }
  };

  const handlePopulateDatabase = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/run/populate-database", {
        method: "POST",
      });
      const result = await res.json();
      alert(result.output || result.error);
    } catch (error) {
      console.error("Error populating database:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleQuery = async (query) => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/run/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const result = await res.json();
      setResponse(result);
    } catch (error) {
      console.error("Error running query:", error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-6 space-y-6">
      <h1 className="text-3xl font-bold text-blue-400">
        Document Uploader & Command Runner
      </h1>
      <div className="w-full max-w-2xl bg-gray-800 p-6 rounded-lg shadow-lg relative">
        {/* Loader Overlay */}
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75 z-50">
            <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-green-500"></div>
          </div>
        )}

        <FileUpload />
        <CommandButtons onInstall={handleInstallRequirements} onPopulate={handlePopulateDatabase} />
        <QueryForm onQuery={handleQuery} />
        <ChangePrompt />
        <QueryResponse response={response} />
      </div>
    </div>
  );
};

export default Home;
