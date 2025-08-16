import React, { useState } from 'react';
import { TreeNode } from '../types/types';
import { FiChevronRight, FiChevronDown } from 'react-icons/fi'; // ✅ Icon imports

export interface CollapsibleTreeProps {
   node: TreeNode;
}

export const CollapsibleTree: React.FC<CollapsibleTreeProps> = ({ node }) => {
   const [isOpen, setIsOpen] = useState(true);
   const hasChildren = node.children && node.children.length > 0;

   return (
      <div className="pl-4 border-l border-gray-300 mb-2">
         <div
            onClick={() => hasChildren && setIsOpen(!isOpen)}
            className="flex items-center cursor-pointer font-semibold text-gray-800 space-x-1"
         >
            {hasChildren ? (
               isOpen ? (
                  <FiChevronDown size={16} />
               ) : (
                  <FiChevronRight size={16} />
               )
            ) : (
               <span className="w-4" />
            )}
            <span>{node.name}</span>
         </div>

         {isOpen && (
            <div className="ml-4 mt-1 text-sm text-gray-700 space-y-1">
               {node.content && <p>{node.content}</p>}
               {node.children?.map((child, index) => (
                  <CollapsibleTree key={index} node={child} />
               ))}
            </div>
         )}
      </div>
   );
};
