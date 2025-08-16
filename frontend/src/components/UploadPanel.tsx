import React, { useEffect, useRef, useState } from 'react';
import { Loader } from './Loader';
import { SearchResultResponse, UploadResultResponse } from '../types/types';

import { UploadResult } from './UploadResult';
import { SearchBar } from './Searchbar';
import { SearchResultChat } from './SearchResultChat';
import { LoadingDots } from './LoadingDots';
import { RecentQueries } from './RecentQueries';
import { FileUploadBox } from './FileUploadBox';

export const UploadPanel: React.FC = () => {
   const [selectedFile, setSelectedFile] = useState<File | null>(null);
   const [isUploading, setIsUploading] = useState(false);
   const [result, setResult] = useState<UploadResultResponse | null>(null);
   const [searchQuery, setSearchQuery] = useState('');
   const [isSearching, setIsSearching] = useState(false);
   const searchResultRef = useRef<HTMLDivElement>(null);
   const isSearchingRef = useRef<HTMLDivElement>(null);
   const [lastUploadedFilename, setLastUploadedFilename] = useState<string | null>(null);
   const [uploadErrorMessage, setUploadErrorMessage] = useState<string | null>(null);
   const [chatHistory, setChatHistory] = useState<
      { query: string; result: SearchResultResponse }[]
   >([]);

   const [recentQueries, setRecentQueries] = useState<string[]>(() => {
      const stored = localStorage.getItem('recentQueries');
      return stored ? JSON.parse(stored) : [];
   });

   useEffect(() => {
      if (chatHistory.length > 0 && searchResultRef.current) {
         searchResultRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
      }
   }, [chatHistory]);

   useEffect(() => {
      if (isSearching && isSearchingRef.current) {
         isSearchingRef.current.scrollIntoView({ behavior: 'smooth' });
      }
   }, [isSearching]);

   const handleUpload = async () => {
      if (!selectedFile) {
         alert('No file selected');
         return;
      }

      if (selectedFile.name === lastUploadedFilename) {
         setUploadErrorMessage('This file has already been uploaded.');
         return;
      }

      setUploadErrorMessage(null);
      setIsUploading(true);
      setResult(null);

      try {
         const formData = new FormData();
         formData.append('file', selectedFile);

         const response = await fetch('http://13.203.228.186:8000/api/upload_codebase', {
            method: 'POST',
            body: formData,
         });

         if (!response.ok) {
            throw new Error('Upload failed with status ' + response.status);
         }

         const data = await response.json();
         setResult(data);
         setLastUploadedFilename(selectedFile.name);
         setSelectedFile(null);
      } catch (err: any) {
         console.error(err);
         alert(err.message || 'Upload failed. Try again.');
      } finally {
         setIsUploading(false);
      }
   };

   const handleSearch = async (e: React.FormEvent, query: string) => {
      e.preventDefault();
      if (!query.trim()) return;

      setIsSearching(true);

      try {
         const response = await fetch('http://13.203.228.186:8000/api/search', {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: query }),
         });

         if (!response.ok) {
            throw new Error(`Search failed with status ${response.status}`);
         }

         const data: SearchResultResponse = await response.json();

         setChatHistory((prev) => [...prev, { query, result: data }]);

         setRecentQueries((prev) => {
            const updated = [query, ...prev.filter((q) => q !== query)].slice(0, 5);
            localStorage.setItem('recentQueries', JSON.stringify(updated));
            return updated;
         });
      } catch (err) {
         console.error('Search failed:', err);
         alert('Something went wrong during search.');
      } finally {
         setIsSearching(false);
      }
   };


   return (
      <div className="relative w-full h-[calc(100vh-96px)] flex text-black">
         {/* Sidebar */}
         <aside className="fixed top-24 left-0 h-[calc(100vh-6rem)] w-64 p-4 bg-gray-100 border-r border-gray-300 overflow-y-auto z-10">
            <h2 className="pt-2 text-2xl font-semibold text-center mb-3">Recent Queries</h2>
            <RecentQueries
               queries={recentQueries}
               onSelectQuery={(query) => {
                  setSearchQuery(query);
                  handleSearch(
                     {
                        preventDefault: () => {},
                        stopPropagation: () => {},
                     } as React.FormEvent,
                     query
                  );
               }}
            />
         </aside>

         {/* Main Content */}
         <div className="flex-1 flex flex-col pl-64">
            {/* Fixed Upload & Search */}
            <div className="absolute top-10 left-64 right-0 bg-white z-10 border-b px-1 pt-2 pb-1">
               <div className="max-w-4xl w-full mx-auto">
                  <FileUploadBox
                     onFileSelect={(file) => setSelectedFile(file)}
                     onUpload={handleUpload}
                     isUploading={isUploading}
                  />

                  {uploadErrorMessage && (
                     <p className="text-red-400 text-sm mt-2 text-center">{uploadErrorMessage}</p>
                  )}

                  {isUploading && (
                     <div className="flex justify-center mt-2">
                        <Loader />
                     </div>
                  )}

                  {/* Upload result (optional) */}
                  {result && <UploadResult result={result} />}

                  {/* ✅ Loading dots BELOW upload result and ABOVE search bar */}
                  {isSearching && chatHistory.length === 0 && (
                     <div
                        ref={isSearchingRef}
                        className="flex justify-start items-center p-4 mb-2 mt-2"
                     >
                        <LoadingDots />
                     </div>
                  )}

                  <div className="mt-4">
                     <SearchBar
                        query={searchQuery}
                        onQueryChange={setSearchQuery}
                        onSubmit={(e, query) => handleSearch(e, query)}
                     />
                  </div>
               </div>
            </div>

            {/* Scrollable Result Area */}

            <div
               className="flex-1 overflow-y-auto mt-[180px] px-4 max-w-4xl w-full mx-auto"
               style={{ paddingBottom: '6rem' }}
            >
               <div ref={searchResultRef} className="space-y-6">
                  {chatHistory.map((entry, index) => (
                     <div key={index}>
                        <div className="mb-1 text-sm text-gray-600">You asked:</div>
                        <div className="bg-gray-200 p-2 rounded-md mb-2 font-medium">
                           {entry.query}
                        </div>
                        <SearchResultChat result={entry.result} />
                     </div>
                  ))}

                  {/* Show loading dots BELOW latest result if chat history exists */}
                  {isSearching && chatHistory.length > 0 && (
                     <div
                        ref={isSearchingRef}
                        className="flex justify-start items-center p-4 mb-6 mt-2"
                     >
                        <LoadingDots />
                     </div>
                  )}
               </div>
            </div>
         </div>
      </div>
   );
};
