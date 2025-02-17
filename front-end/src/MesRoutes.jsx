import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/header";
import PageFound from "./components/PageFound";
import Register from "./components/Register";
import Login from "./components/Login";
import Profile from "./components/Profile";
import AddVehicule from "./components/AddVehicule";
import ListVehicules from "./components/ListVehicules";
import DetailVehicule from "./components/DetailVehicule";
import Annonce from "./components/Annonce";
import Accueil from "./components/Accueil";
import Acheter from "./components/Acheter";
import VehicleDetails from "./components/VehicleDetails";

export default function MesRoutes() {
  return (
    <BrowserRouter>
      <div>
        <Header />
        <main className="p-4">
          <Routes>
              {/* <Route path="register" element={<Register />} /> */}
              <Route path="/" element={<Accueil/>} />
              <Route path="register-page" element={<Register />} />
              <Route path="login-page" element={<Login/>} />
              <Route path="profile-page" element={<Profile/>} />
              <Route path="vehicle-details" element={<VehicleDetails/>} />
              <Route path="addVehicule" element={<AddVehicule />} />
              <Route path="vehicules" element={<ListVehicules />} />
              <Route path="vehicules/:id" element={<DetailVehicule />} />
              <Route path="annonce" element={<Annonce />} />
              
              <Route path="*" element={<PageFound />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
