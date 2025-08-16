import React from 'react';

interface RecentQueriesProps {
   queries: string[];
   onSelectQuery: (query: string) => void;
}

export const RecentQueries: React.FC<RecentQueriesProps> = ({ queries, onSelectQuery }) => {
   if (queries.length === 0) return null;

   return (
      <div className="max-w-4xl mx-auto px-4 mt-4">
         <div className="flex flex-wrap gap-2">
            {queries.map((query, idx) => (
               <button
                  key={idx}
                  onClick={() => onSelectQuery(query)}
                  className="bg-blue-900 hover:bg-blue-800 text-white text-sm px-4 py-2 rounded-full max-w-xs truncate"
                  title={query} // shows full query on hover
               >
                  {query}
               </button>
            ))}
         </div>
      </div>
   );
};
