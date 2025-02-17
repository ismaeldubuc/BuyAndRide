import { BrowserRouter, Routes, Route } from "react-router-dom";

import PageFound from "./components/PageFound";
import Register from "./components/Register";
import Login from "./components/login";
import Profile from "./components/Profile";
import Acheter from "./components/Acheter";

export default function MesRoutes() {
  return (
    <BrowserRouter>
      <Routes>       
          <Route path="register-page" element={<Register />} />
          <Route path="login-page" element={<Login />} />
          <Route path="profile-page" element={<Profile/>} />
          <Route path="acheter-page" element={<Acheter/>} />
          <Route path="*" element={<PageFound />} />
      </Routes>
    </BrowserRouter>
  );
}