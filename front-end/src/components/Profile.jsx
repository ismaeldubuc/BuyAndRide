import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { API_URL, STATIC_URL } from "../config";

function Profile() {
  const [vehicules, setVehicules] = useState([]);
  const [error, setError] = useState(null);
  const [userData, setUserData] = useState(null);

  const [user, setUser] = useState({
    nom: "",
    prenom: "",
    email: "",
  });

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(`${API_URL}/check-login`, {
          credentials: "include",
        });
        const data = await response.json();
        setUserData(data);
      } catch (error) {
        console.error("Erreur:", error);
      }
    };

    fetchUserData();
  }, []);

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
              email: dataArray[2],
            };
            setUser(userData);
          } else {
            console.error("Format des données reçues inattendu:", dataArray);
            setError("Format des données incorrect.");
          }
        } else {
          setError(
            dataArray.error || "Impossible de récupérer les informations."
          );
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
  // console.log("userId:", userId);

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
        setVehicules(response.data);
      } catch (error) {
        console.error("Error fetching vehicles:", error);
      }
    };

    fetchVehicules();
  }, []);

  const getImageUrl = (photoUrl) => {
    if (!photoUrl) return null;
    console.log("Traitement de l'URL:", photoUrl);

    // Si c'est une URL S3
    if (photoUrl.includes("s3.amazonaws.com")) {
      return photoUrl;
    }

    // Si c'est un chemin local
    return `${STATIC_URL}/${photoUrl}`;
  };

  if (error) {
    return <div>Erreur: {error}</div>;
  }

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
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Mes Véhicules</h1>
          <Link
            to="/addVehicule"
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            + Ajouter un véhicule
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {vehicules.map((vehicule) => (
            <div
              key={vehicule.id}
              className="bg-white rounded-lg shadow-md overflow-hidden"
            >
              <div className="image-container">
                {vehicule.photo1 && (
                  <img
                    src={vehicule.photo1}
                    alt={`${vehicule.marque} ${vehicule.modele}`}
                    className="w-full h-48 object-cover"
                    onError={(e) => {
                      console.error(
                        `Erreur de chargement de l'image:`,
                        vehicule.photo1
                      );
                      e.target.src = "/src/assets/placeholder.png";
                    }}
                  />
                )}
              </div>
              <div className="p-4">
                <h2 className="text-xl font-semibold">
                  {vehicule.marque} {vehicule.modele}
                </h2>
                <p className="text-gray-600">{vehicule.prix} €</p>
                <p className="text-gray-500">{vehicule.km} km</p>
                <p className="text-gray-500">{vehicule.energie}</p>
                <Link
                  to={`/vehicules/${vehicule.id}`}
                  className="mt-2 inline-block bg-blue-500 text-white px-4 py-2 rounded"
                >
                  Voir détails
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
export default Profile;
