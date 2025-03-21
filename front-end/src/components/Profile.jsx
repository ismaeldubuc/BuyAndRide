import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { API_URL } from '../config';

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
        const response = await fetch(`${API_URL}/profile`, {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
        });
  
        const dataArray = await response.json();  
        if (response.ok) {
          if (dataArray.length === 3) {
            const userData = {
              nom: dataArray[0],
              prenom: dataArray[1],
              email: dataArray[2]
            };
            setUser(userData);
          } else {
            console.error("Format des données reçues inattendu:", dataArray);
            setError("Format des données incorrect.");
          }
        } else {
          setError(dataArray.error || "Impossible de récupérer les informations.");
        }
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
        setError("Erreur serveur.");
      }
    };
  
    fetchProfile();
  }, []);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setUser((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  
  const userId = localStorage.getItem("userId");
  console.log("userId:", userId);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      const response = await fetch(`${API_URL}/modif_profil`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams(user),
        credentials: "include",
      });

      if (response.ok) {
        setMessage("Profil mis à jour !");
        setIsEditing(false);
      } else {
        const data = await response.text();
        setError(data || "Erreur lors de la mise à jour.");
      }
    } catch (error) {
      setError("Erreur serveur.");
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    if (passwords.new_password !== passwords.confirm_password) {
      setError("Les mots de passe ne correspondent pas.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/modif_profil`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          changer_mdp: "true",
          new_password: passwords.new_password,
          confirm_password: passwords.confirm_password,
        }),
        credentials: "include",
      });

      const data = await response.text();
      if (response.ok) {
        setMessage("Mot de passe mis à jour !");
        setIsChangingPassword(false);
        setPasswords({ new_password: "", confirm_password: "" });
      } else {
        setError(data || "Erreur lors de la mise à jour.");
      }
    } catch (error) {
      setError("Erreur serveur.");
    }
  };

  const handleLogout = async () => {
    try {
      const response = await fetch(`${API_URL}/logout`, {
        method: "POST",
        credentials: "include",
      });

      if (response.ok) {
        navigate("/login-page");
      } else {
        console.error("Erreur lors de la déconnexion");
      }
    } catch (error) {
      console.error("Erreur:", error);
    }
  };
  useEffect(() => {
    const fetchVehicules = async () => {
      
      try {
        const response = await axios.get(`${API_URL}/vehicules`, {
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
                <p className="text-gray-500">{vehicule.km} km</p>
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
            <Link to="/addVehicule" className="p-8">
              <div className="w-24 h-24 bg-blue-500 rounded-full flex items-center justify-center hover:bg-blue-600 transition-colors">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-12 w-12 text-white"
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
