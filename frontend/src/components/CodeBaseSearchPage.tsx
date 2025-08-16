import { UploadPanel } from './UploadPanel';

export const CodebaseSearchPage: React.FC = () => {
   return (
      <main className="min-h-screen text-black flex flex-col">
         <div className="sticky top-0 z-20 flex justify-between items-center py-4 px-6 bg-white shadow">
            {/* Logo aligned left */}
            <div className="flex items-center gap-4">
               <img src="/logo.png" alt="CodeCoach Logo" className="w-20 h-20" />
               <div>
                  <h1 className="text-2xl font-bold">Smart Codebase Search</h1>
                  <p className="text-gray-500 text-sm">Your own Onboarding Buddy!!</p>
               </div>
            </div>
         </div>

         {/* ✅ No overflow or margin here */}
         <UploadPanel />
      </main>
   );
};
