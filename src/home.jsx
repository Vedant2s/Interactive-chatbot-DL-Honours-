import React, { useState } from "react";

const Home = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [file, setFile] = useState(null);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });
      const result = await res.json();
      alert(result.message);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const handleInstallRequirements = async () => {
    try {
      const res = await fetch(
        "http://localhost:5000/run/install-requirements",
        {
          method: "POST",
        }
      );
      const result = await res.json();
      alert(result.output || result.error);
    } catch (error) {
      console.error("Error installing requirements:", error);
    }
  };

  const handlePopulateDatabase = async () => {
    try {
      const res = await fetch("http://localhost:5000/run/populate-database", {
        method: "POST",
      });
      const result = await res.json();
      alert(result.output || result.error);
    } catch (error) {
      console.error("Error populating database:", error);
    }
  };

  const handleQuery = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:5000/run/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });
      const result = await res.json();
      setResponse(result);
    } catch (error) {
      console.error("Error running query:", error);
    }
  };

  return (
    <div>
      <h1>Document Uploader and Command Runner</h1>

      <form onSubmit={handleFileUpload}>
        <label htmlFor="file">Upload Document:</label>
        <input
          type="file"
          id="file"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit">Upload</button>
      </form>

      <div>
        <button onClick={handleInstallRequirements}>
          Install Requirements
        </button>
        <button onClick={handlePopulateDatabase}>Populate Database</button>
      </div>

      <form onSubmit={handleQuery}>
        <label htmlFor="query">Enter Query:</label>
        <input
          type="text"
          id="query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Run Query</button>
      </form>

      {response && (
        <div>
          <h2>Query Response</h2>
          <pre style={{ overflow: "auto", whiteSpace: "pre-wrap" }}>
            {response.output || "No output available"}
          </pre>
        </div>
      )}
    </div>
  );
};

export default Home;
