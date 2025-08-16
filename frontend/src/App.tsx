import React, { useEffect } from 'react';
import { CodebaseSearchPage } from './components/CodeBaseSearchPage';

function App() {
   useEffect(() => {
      localStorage.removeItem('recentQueries');
   }, []);
   return <CodebaseSearchPage />;
}

export default App;
