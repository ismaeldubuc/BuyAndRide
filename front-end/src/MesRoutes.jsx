import { BrowserRouter, Routes, Route } from "react-router-dom";

import PageFound from "./components/PageFound";
import Register from "./components/Register";
import Login from "./components/login";
import Profile from "./components/Profile";
import AddVehicule from "./components/AddVehicule";
import ListVehicules from "./components/ListVehicules";
import DetailVehicule from "./components/DetailVehicule";
import Annonce from "./components/Annonce";

export default function MesRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="register-page" element={<Register />} />
        <Route path="login-page" element={<Login />} />
        <Route path="profile-page" element={<Profile />} />
        <Route path="addVehicule" element={<AddVehicule />} />
        <Route path="vehicules" element={<ListVehicules />} />
        <Route path="vehicules/:id" element={<DetailVehicule />} />
        <Route path="annonce" element={<Annonce />} />

        <Route path="*" element={<PageFound />} />
      </Routes>
    </BrowserRouter>
  );
}
