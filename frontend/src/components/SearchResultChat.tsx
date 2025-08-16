import React, { useState } from 'react';
import { SearchResultResponse } from '../types/types';
import { FiCopy, FiCheck } from 'react-icons/fi';

interface Props {
   result: SearchResultResponse;
}

export const SearchResultChat: React.FC<Props> = ({ result }) => {
   const [copied, setCopied] = useState(false);

   const handleCopy = () => {
      const textToCopy = `
AI Response

Summary:
${result.answer}

Related Files:
${result.related_files.join('\n')}
      `.trim();

      navigator.clipboard.writeText(textToCopy);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
   };

   return (
      <div className="relative bg-white border border-gray-300 rounded-lg p-4 max-w-4xl mx-auto mb-6 mt-4 shadow-md">
         {/* Copy button */}
         <button
            onClick={handleCopy}
            title="Copy Response"
            className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
         >
            {copied ? <FiCheck size={18} /> : <FiCopy size={18} />}
         </button>

         <h2 className="text-xl font-semibold text-blue-600 mb-4">AI Response</h2>

         <div className="space-y-4 text-gray-800 text-sm">
            <div>
               <h3 className="font-semibold mb-1">Summary</h3>
               <p className="whitespace-pre-line">{result.answer}</p>
            </div>

            <div>
               <h3 className="font-semibold mb-1">Related Files</h3>
               <ul className="bg-gray-100 rounded p-3 text-sm space-y-1 list-disc list-inside">
                  {result.related_files.map((file, index) => (
                     <li key={index}>{file}</li>
                  ))}
               </ul>
            </div>
         </div>
      </div>
   );
};
