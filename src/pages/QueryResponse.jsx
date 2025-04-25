
import React from "react";
import '../output.css';

const highlightWords = (text, words) => {
  if (!words || words.length === 0) return text;

  const highlightColors = [
    "bg-red-400", "bg-orange-400", "bg-yellow-300",
    "bg-green-300", "bg-blue-300", "bg-purple-300"
  ];

  // Lowercase all words for matching
  const lowerWords = words.map(w => w.toLowerCase());
  const escaped = lowerWords.map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const regex = new RegExp(`(${escaped.join("|")})`, "gi");

  return text.split(regex).map((part, i) => {
    const low = part.toLowerCase();
    const idx = lowerWords.indexOf(low);
    if (idx !== -1) {
      const colorClass = highlightColors[idx % highlightColors.length];
      return (
        <span
          key={i}
          className={`${colorClass} text-black font-semibold rounded px-1 mr-1`}
        >
          {part}
        </span>
      );
    }
    return part;
  });
};

const QueryResponse = ({ response }) => {
  if (!response) return null;

  const {
    output = "No output available",
    top_contributing_words = [],
    // context = "" // Context remains unchanged and not highlighted
  } = response;

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg mt-4 text-white w-full">
      <h2 className="text-xl font-bold text-blue-400">Query Response</h2>

      {/* Highlighted Output */}
      <div className="bg-gray-900 p-4 rounded-md mt-2 overflow-auto whitespace-pre-wrap text-green-400">
        {highlightWords(output, top_contributing_words)} {/* Highlight only the answer */}
      </div>

      
    </div>
  );
};

export default QueryResponse;
