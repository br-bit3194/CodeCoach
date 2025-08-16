interface ImportMetaEnv {
   readonly VITE_BACKEND_URL: string;
   // add other env variables you use here...
}

interface ImportMeta {
   readonly env: ImportMetaEnv;
}
