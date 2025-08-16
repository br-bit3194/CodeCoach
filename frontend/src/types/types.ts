export type TreeNode = {
   name: string;
   content?: string;
   children?: TreeNode[];
};

export interface UploadTreeResult {
   summary: TreeNode;
   prdDoc: TreeNode;
}

export interface UploadSection {
   type: 'section' | 'point';
   title: string;
   content?: string;
   children?: UploadSection[];
}

export interface UploadSectionResult {
   summary: UploadSection;
   prdDoc: UploadSection;
}

export interface SearchResultResponse {
   answer: string;
   related_files: string[];
}

export interface UploadResultResponse {
   prdDoc: string; // now a URL instead of nested structure
}
