import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";

import MesRoutes from "./MesRoutes.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <MesRoutes />
  </StrictMode>
);
