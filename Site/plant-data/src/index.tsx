import App from "./App"
import React from 'react';
import ReactDOM from 'react-dom/client';

const rootElement = document.getElementById('root');

// Ensure the root element exists before attempting to render
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
      <React.StrictMode>
          <App />
      </React.StrictMode>
  );
} else {
  console.error("Root element not found. Ensure you have a div with id 'root' in your HTML.");
}


