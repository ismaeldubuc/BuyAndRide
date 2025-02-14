import { BrowserRouter, Routes, Route } from "react-router-dom";

import PageFound from "./components/PageFound";
import Register from "./components/Register";
import Login from "./components/login";
import Profile from "./components/Profile";

export default function MesRoutes() {
  return (
    <BrowserRouter>
      <Routes>
          {/* <Route path="register" element={<Register />} /> */}
          <Route path="register-page" element={<Register />} />
          <Route path="login-page" element={<Login/>} />
          <Route path="profile-page" element={<Profile/>} />
          
          <Route path="*" element={<PageFound />} />
      </Routes>
    </BrowserRouter>
  );
}