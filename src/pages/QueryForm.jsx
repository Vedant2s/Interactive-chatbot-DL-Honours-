import React, { useState, useRef } from "react";
import '../output.css';

const QueryForm = ({ onQuery }) => {
  const [query, setQuery] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const recognitionRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    await onQuery(query);
    setIsLoading(false);
  };

  const toggleRecording = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech recognition is not supported in this browser.');
      return;
    }

    if (isRecording) {
      recognitionRef.current.stop();
      setIsRecording(false);
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => setIsRecording(true);
    recognition.onerror = (event) => console.error("Speech Recognition Error:", event);
    recognition.onend = () => setIsRecording(false);
    recognition.onresult = (event) => {
      let transcript = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      setQuery(transcript);
    };

    recognition.start();
    recognitionRef.current = recognition;
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col items-center space-y-4">
      <label htmlFor="query" className="text-white text-lg font-bold">Enter Query:</label>
      <input 
        type="text" 
        id="query" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        className="p-2 border border-gray-600 rounded-md bg-gray-900 text-white w-full"
      />
      <button 
        type="button" 
        onClick={toggleRecording} 
        className={`px-6 py-2 rounded-lg shadow-lg transition duration-300 ${isRecording ? 'bg-red-500' : 'bg-blue-500'} text-white hover:opacity-80`}
      >
        🎤 {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
      <button 
        type="submit" 
        className="bg-purple-500 text-white px-6 py-2 rounded-lg shadow-lg hover:bg-purple-600 transition duration-300"
      >
        🔍 Run Query
      </button>
      {isLoading && <div className="w-10 h-10 border-4 border-green-500 border-dashed rounded-full animate-spin mt-4"></div>}
    </form>
  );
};

export default QueryForm;
