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

// import React from "react";

// const QueryResponse = ({ response }) => {
//   if (!response) return null;

//   return (
//     <div className="mt-6 bg-gray-900 p-4 rounded-lg shadow-lg text-white space-y-4">
//       <h2 className="text-xl font-bold text-green-400">🧠 Answer:</h2>
//       <p>{response.answer}</p>
// {/* 
//       {response.sources && response.sources.length > 0 && (
//         <>
//           <h3 className="text-lg font-semibold text-yellow-400">📚 Sources:</h3>
//           <ul className="list-disc list-inside">
//             {response.sources.map((src, i) => (
//               <li key={i}>{src}</li>
//             ))}
//           </ul>
//         </>
//       )}

//       {response.image_caption && (
//         <>
//           <h3 className="text-lg font-semibold text-blue-400">🖼️ Image Caption:</h3>
//           <p>{response.image_caption}</p>
//         </>
//       )} */}
//     </div>
//   );
// };

// export default QueryResponse;