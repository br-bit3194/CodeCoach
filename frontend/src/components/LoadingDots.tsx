export const LoadingDots: React.FC = () => (
   <span className="inline-flex items-center space-x-1">
      <span className="block w-3 h-3 bg-black rounded-full animate-bounce delay-300 duration-500" />
      <span className="block w-3 h-3 bg-black rounded-full animate-bounce delay-600 duration-500" />
      <span className="block w-3 h-3 bg-black rounded-full animate-bounce delay-900 duration-500" />
   </span>
);
