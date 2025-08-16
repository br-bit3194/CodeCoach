import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { UploadResultResponse } from '../types/types';

interface UploadResultProps {
   result: UploadResultResponse;
}

export const UploadResult: React.FC<UploadResultProps> = ({ result }) => {
   const [prdContent, setPrdContent] = useState<string | null>(null);
   const [loading, setLoading] = useState(false);
   const [error, setError] = useState<string | null>(null);

   useEffect(() => {
      const loadMarkdown = async () => {
         if (!result?.prdDoc) return;

         setLoading(true);
         try {
            const res = await fetch(result.prdDoc); // `prdDoc` should be a valid URL
            if (!res.ok) throw new Error('Failed to fetch PRD markdown');
            const text = await res.text();
            setPrdContent(text);
         } catch (err: any) {
            setError(err.message);
         } finally {
            setLoading(false);
         }
      };

      loadMarkdown();
   }, [result]);

   return (
      <div className="p-6 bg-white shadow-md rounded-lg max-w-4xl mx-auto">
         <h2 className="text-xl font-bold text-gray-800 mb-4">📄 PRD Document Preview</h2>

         {!result.prdDoc && (
            <p className="text-gray-600">No PRD document found in the uploaded codebase.</p>
         )}

         {loading && <p className="text-gray-500">Loading PRD content...</p>}
         {error && <p className="text-red-500">Error: {error}</p>}
         {prdContent && (
            <div className="prose prose-sm max-w-none text-gray-800">
               <ReactMarkdown>{prdContent}</ReactMarkdown>
            </div>
         )}
      </div>
   );
};
