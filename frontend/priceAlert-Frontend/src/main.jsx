import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

// Uncomment the line below to test with a simple app first
// import App from "./SimpleApp.jsx";
import App from "./App.jsx";

console.log("Main.jsx loaded - starting React initialization");

const rootElement = document.getElementById("root");

if (!rootElement) {
  document.body.innerHTML =
    '<h1 style="color: red; padding: 20px;">Error: Root element not found!</h1>';
  throw new Error("Root element not found");
}

console.log("Root element found, attempting to render...");

try {
  const root = createRoot(rootElement);
  console.log("React root created");

  root.render(
    <StrictMode>
      <App />
    </StrictMode>
  );

  console.log("App render called successfully");
} catch (error) {
  console.error("Error rendering app:", error);
  rootElement.innerHTML = `
    <div style="padding: 20px; font-family: Arial; background: #fee; border: 2px solid red; margin: 20px;">
      <h1 style="color: red;">Error Loading App</h1>
      <p><strong>Error:</strong> ${error.message}</p>
      <pre style="background: #f5f5f5; padding: 10px; overflow: auto; max-height: 400px; overflow-y: auto;">${error.stack}</pre>
      <p style="margin-top: 20px;"><strong>Check the browser console (F12) for more details.</strong></p>
    </div>
  `;
}
