import { UploadSection, UploadTreeResult } from '../types/types';
import { TreeNode } from '../types/types';

export const transformUploadSectionToTree = (section: UploadSection): TreeNode => {
   const node: TreeNode = {
      name: section.title,
      content: section.content,
      children: section.children?.map(transformUploadSectionToTree),
   };
   return node;
};
