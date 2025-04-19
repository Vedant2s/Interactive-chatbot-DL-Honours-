import React, { useState } from 'react';

const ChangePrompt = () => {
  const [promptTemplate, setPromptTemplate] = useState("");
  const [status, setStatus] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Update the URL to point to the Flask server on port 5000.
      const response = await fetch('http://localhost:5000/run/update-prompt-template', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt_template: promptTemplate }),
      });

      const data = await response.json();

      if (response.ok) {
        setStatus({ success: true, message: data.message });
      } else {
        setStatus({ success: false, message: data.message });
      }
    } catch (error) {
      setStatus({ success: false, message: error.toString() });
    }
  };

  return (
    <div className="min-h-full flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 p-6">
      <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-xl">
        <h2 className="text-2xl font-bold mb-6 text-center">Update Prompt Template</h2>
        <form onSubmit={handleSubmit}>
          <textarea
            value={promptTemplate}
            onChange={(e) => setPromptTemplate(e.target.value)}
            placeholder="Enter your new prompt template. Use {context} and {question} as placeholders."
            rows="3"
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
          />
          <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded-lg transition duration-200"
          >
            Update Prompt Template
          </button>
        </form>
        {status && (
          <div
            className={`mt-4 p-3 text-center rounded-lg ${status.success ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}
          >
            {status.message}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChangePrompt;
