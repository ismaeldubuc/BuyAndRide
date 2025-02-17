import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/header";
import PageFound from "./components/PageFound";
import Register from "./components/Register";
import Login from "./components/login";
import Profile from "./components/Profile";
import VehicleDetails from "./components/VehicleDetails";

export default function MesRoutes() {
  return (
    <BrowserRouter>
      <div>
        <Header />
        <main className="p-4">
          <Routes>
              {/* <Route path="register" element={<Register />} /> */}
              <Route path="register-page" element={<Register />} />
              <Route path="login-page" element={<Login/>} />
              <Route path="profile-page" element={<Profile/>} />
              <Route path="vehicle-details" element={<VehicleDetails/>} />
              
              <Route path="*" element={<PageFound />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}