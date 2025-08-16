import React, { useEffect, useRef, useState } from 'react';
import { FiSearch } from 'react-icons/fi';

interface SemanticSearchBarProps {
   query: string;
   onQueryChange: (value: string) => void;
   onSubmit: (e: React.FormEvent, query: string) => void; // pass query explicitly
}

export const SearchBar: React.FC<SemanticSearchBarProps> = ({ query, onQueryChange, onSubmit }) => {
   const inputRef = useRef<HTMLInputElement>(null);
   const [localQuery, setLocalQuery] = useState(query);

   // Autofocus on mount
   useEffect(() => {
      inputRef.current?.focus();
   }, []);

   // Sync localQuery with query prop changes
   useEffect(() => {
      setLocalQuery(query);
   }, [query]);

   const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault();
      if (!localQuery.trim()) return;
      onSubmit(e, localQuery);
      setLocalQuery('');
      onQueryChange('');
      inputRef.current?.blur(); // defocus input after submit
   };

   const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setLocalQuery(e.target.value);
      onQueryChange(e.target.value);
   };

   return (
      <form
         onSubmit={handleSubmit}
         className="bg-white fixed bottom-0 left-64 right-0 px-4 py-4 border-t border-gray-700 z-20"
      >
         <div className="bg-white max-w-4xl mx-auto flex gap-4 items-center">
            <div className="relative flex-1">
               <FiSearch className="absolute left-3 top-2.5 text-gray-400" size={20} />
               <input
                  ref={inputRef}
                  type="text"
                  value={localQuery}
                  onChange={handleChange}
                  placeholder="e.g., Where is the data fetched for the dashboard? 🔍"
                  className="bg-white w-full text-black pl-10 pr-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-grey-300"
               />
            </div>
            <button
               type="submit"
               className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
               Search
            </button>
         </div>
      </form>
   );
};
