import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { API_URL } from '../config';

function UpdateProfile() {
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  const [user, setUser] = useState({
    nom: "",
    prenom: "",
    email: "",
    password: "",
  });

  const [passwords, setPasswords] = useState({
    new_password: "",
    confirm_password: "",
  });

  const navigate = useNavigate();

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
              password: dataArray[3]
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

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswords((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
        const userData = { ...user };
        if (!userData.password) {
            delete userData.password;
        }

        const response = await fetch(`${API_URL}/modif_profil`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            credentials: "include",
            body: JSON.stringify(userData)
        });

        const data = await response.json();

        if (response.ok) {
            setMessage("Profil mis à jour avec succès !");
            setUser(prev => ({
                ...prev,
                password: ''
            }));
        } else {
            setError(data.error || "Erreur lors de la mise à jour du profil");
        }
    } catch (error) {
        console.error("Erreur:", error);
        setError("Erreur de connexion au serveur");
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
      const response = await fetch("http://localhost:8000/profile", {
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
            credentials: "include"
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

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-3xl dark:bg-gray-800">
        <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
          Modifier mon profil
        </h1>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        {message && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-900 dark:text-white mb-1">
                Nom
              </label>
              <input
                type="text"
                name="nom"
                value={user.nom}
                onChange={handleChange}
                className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-900 dark:text-white mb-1">
                Prénom
              </label>
              <input
                type="text"
                name="prenom"
                value={user.prenom}
                onChange={handleChange}
                className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 dark:text-white mb-1">
              Email
            </label>
            <input
              type="email"
              name="email"
              value={user.email}
              onChange={handleChange}
              className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 dark:text-white mb-1">
              Nouveau mot de passe
            </label>
            <div className="relative">
              <input
                type={showNewPassword ? "text" : "password"}
                name="password"
                value={user.password || ''}
                onChange={handleChange}
                className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
              <button
                type="button"
                onClick={() => setShowNewPassword(!showNewPassword)}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500"
              >
                {showNewPassword ? "Masquer" : "Afficher"}
              </button>
            </div>
          </div>

          <div className="flex justify-between">
            <button
              type="submit"
              className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              Mettre à jour
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default UpdateProfile;
