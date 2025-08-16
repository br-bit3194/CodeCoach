import React, { useRef, useState, useEffect } from 'react';

interface FileUploadBoxProps {
   onFileSelect: (file: File) => void;
   onUpload: () => void;
   isUploading: boolean;
}

export const FileUploadBox: React.FC<FileUploadBoxProps> = ({
   onFileSelect,
   onUpload,
   isUploading,
}) => {
   const fileInputRef = useRef<HTMLInputElement>(null);
   const [fileName, setFileName] = useState<string | null>(null);
   const [hasUploaded, setHasUploaded] = useState(false);

   useEffect(() => {
      if (!isUploading && fileName && hasUploaded) {
         // Reset file name after successful upload
         const timer = setTimeout(() => {
            setFileName(null);
            setHasUploaded(false);
         }, 500); // Delay to allow success indication (optional)
         return () => clearTimeout(timer);
      }
   }, [isUploading, fileName, hasUploaded]);

   const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      const file = e.dataTransfer.files?.[0];
      if (file && file.name.endsWith('.zip')) {
         setFileName(file.name);
         onFileSelect(file);
         setHasUploaded(false);
      } else {
         alert('Only .zip files are supported');
      }
   };

   const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file && file.name.endsWith('.zip')) {
         setFileName(file.name);
         onFileSelect(file);
         setHasUploaded(false);
      } else {
         alert('Only .zip files are supported');
      }
   };

   const handleUploadClick = () => {
      onUpload();
      setHasUploaded(true);
   };

   return (
      <div className="w-full flex items-start gap-1 flex-wrap sm:flex-nowrap">
         {/* Upload Box */}
         <div className="flex-1">
            <div
               className=" border border-dashed border-gray-400 rounded-md px-3 py-2 text-center bg-blue-50 cursor-pointer hover:bg-blue-100 transition"
               onClick={() => fileInputRef.current?.click()}
               onDrop={handleDrop}
               onDragOver={(e) => e.preventDefault()}
            >
               <input
                  ref={fileInputRef}
                  type="file"
                  accept=".zip"
                  onChange={handleFileChange}
                  className="hidden"
               />
               <div className="flex items-center justify-center gap-2 text-sm text-gray-700">
                  <svg
                     xmlns="http://www.w3.org/2000/svg"
                     className="h-5 w-5 text-blue-500"
                     fill="none"
                     viewBox="0 0 24 24"
                     stroke="currentColor"
                  >
                     <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1M12 12v9m0 0l-3-3m3 3l3-3m4-10a2 2 0 00-2-2H7a2 2 0 00-2 2v4h14V6z"
                     />
                  </svg>
                  <span>
                     Click or drop <strong>.zip codebase</strong> file
                  </span>
               </div>
            </div>

            {/* File Name */}
            <div className="h-6 mt-1 text-sm text-gray-600 text-center truncate">
               {fileName ? (
                  <>
                     Selected: <span className="font-medium">{fileName}</span>
                  </>
               ) : (
                  '\u00A0'
               )}
            </div>
         </div>

         {/* Upload Button (conditionally rendered) */}
         {fileName && !hasUploaded && (
            <button
               onClick={handleUploadClick}
               disabled={isUploading}
               className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 whitespace-nowrap"
            >
               {isUploading ? 'Uploading...' : 'Upload'}
            </button>
         )}
      </div>
   );
};
