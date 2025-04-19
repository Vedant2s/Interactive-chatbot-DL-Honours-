import React, { useState } from "react";
import '../output.css'
const FileUpload = () => {
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

  return (
    <form onSubmit={handleFileUpload} className="bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col items-center space-y-4">
      <label htmlFor="file" className="text-white text-lg font-bold">Upload Document:</label>
      <input 
        type="file" 
        id="file" 
        onChange={(e) => setFile(e.target.files[0])} 
        className="p-2 border border-gray-600 rounded-md bg-gray-900 text-white"
      />
      <button 
        type="submit" 
        className="bg-blue-500  text-white px-6 py-2 rounded-lg shadow-lg hover:bg-blue-600 transition duration-300"
      >
        🚀 Upload
      </button>
    </form>
  );
};

export default FileUpload;
