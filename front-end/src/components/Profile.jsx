import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function Profile() {
  const [vehicules, setVehicules] = useState([]);
  const [error, setError] = useState("");

  const [user, setUser] = useState({
    nom: "",
    prenom: "",
    email: "",
  });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch("http://localhost:8000/profile", {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();
        if (response.ok) {
          setUser(data);
        } else {
          setError(data.error || "Impossible de récupérer les informations.");
        }
      } catch (response) {
        console.log(response.headers);
        setError("Erreur serveur.");
      }
    };

    fetchProfile();
  }, []);

  // affiche liste de vehicules

  
  const userId = localStorage.getItem("userId");
  console.log("userId:", userId);

  useEffect(() => {
    const fetchVehicules = async () => {
      
      try {
        const response = await axios.get(`http://localhost:8000/vehicules`, {
          withCredentials: true,
        });
        console.log("response:", response.data);
        setVehicules(response.data);
      } catch (error) {
        console.error("Error fetching vehicles:", error);
      }
    };
    fetchVehicules();
  }, [userId]);

  return (
    <>
  
      <div className="flex items-center justify-center bg-gray-50 dark:bg-gray-900 p-6">
        <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-3xl dark:bg-gray-800">
          <div className="space-y-6">
            <div className="grid grid-cols-3 gap-6">
              <div className="flex flex-col">
                <label className="block text-sm font-medium text-gray-900 dark:text-white mb-1">
                  Nom
                </label>
                <p className="dark:text-white font-bold dark:bg-gray-700 ">
                  {user.nom}
                </p>
              </div>

              <div className="flex flex-col">
                <label className="block text-sm font-medium text-gray-900 dark:text-white mb-1">
                  Prénom
                </label>
                <p className="dark:text-white font-bold dark:bg-gray-700 ">
                  {user.prenom}
                </p>
              </div>

              <div className="flex flex-col">
                <label className="block text-sm font-medium text-gray-900 dark:text-white mb-1">
                  Email
                </label>
                <p className="dark:text-white font-bold dark:bg-gray-700 ">
                  {user.email}
                </p>
              </div>
            </div>

            <div className="text-center">
              <a
                href="/update-profile"
                className="inline-block px-4 py-2 text-sm font-medium text-white bg-blue-500 rounded hover:bg-blue-600 focus:ring-2 focus:ring-blue-400"
              >
                Modifier mon profil
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6">Mes véhicules</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {vehicules.map((vehicule) => (
            <div
              key={vehicule.id}
              className="bg-white rounded-lg shadow-md overflow-hidden"
            >
              <img
                src={`http://localhost:8000/static/${vehicule.photo1}`}
                alt={`${vehicule.marque} ${vehicule.modele}`}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <h2 className="text-xl font-semibold">
                  {vehicule.marque} {vehicule.modele}
                </h2>
                <p className="text-gray-600">{vehicule.prix} €</p>
                <p className="text-gray-500">{vehicule.kilometrage} km</p>
                <div className="mt-4">
                  <Link
                    to={`/vehicules/${vehicule.id}`}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                  >
                    Voir détails
                  </Link>
                </div>
              </div>
            </div>
          ))}
          <div className="bg-gray-100 rounded-lg shadow-md overflow-hidden flex items-center justify-center">
            <Link to="/login-page" className="p-8">
              <div className="w-50 h-50 bg-blue-500 rounded-full flex items-center justify-center hover:bg-blue-600 transition-colors">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-24 w-24 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 4v16m8-8H4"
                  />
                </svg>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
export default Profile;
