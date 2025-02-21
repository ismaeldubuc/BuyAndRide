import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { API_URL } from '../config';

function Profile() {
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  

  const [user, setUser] = useState({
    nom: "",
    prenom: "",
    email: "",
  });

  const [passwords, setPasswords] = useState({
    new_password: "",
    confirm_password: "",
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`${API_URL}/profile`, {
          method: "GET",
          credentials: "include",
          headers: {
            'Content-Type': 'application/json',
          },
        });
  
        const dataArray = await response.json();  // Assume dataArray is something like ["Dubuc", "Ismael", "ismael.dubuc@gmail.com"]
        if (response.ok) {
          // Conversion du tableau en objet
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

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 p-6">
      <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md dark:bg-gray-800">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
            {isEditing ? "Modifier le profil" : "Mon profil"}
          </h2>
          {!isEditing && (
            <button
              onClick={() => setIsEditing(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Modifier
            </button>
          )}
        </div>

        {message && (
          <div className="p-3 mb-4 text-sm text-green-600 bg-green-100 border border-green-400 rounded-md">
            {message}
          </div>
        )}
        {error && (
          <div className="p-3 mb-4 text-sm text-red-600 bg-red-100 border border-red-400 rounded-md">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-900 dark:text-white">
              Nom
            </label>
            <input
              type="text"
              name="nom"
              value={user.nom}
              onChange={handleChange}
              className="w-full p-2.5 border rounded-lg bg-gray-50 dark:bg-gray-700 dark:text-white"
              required
              disabled={!isEditing}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 dark:text-white">
              Prénom
            </label>
            <input
              type="text"
              name="prenom"
              value={user.prenom}
              onChange={handleChange}
              className="w-full p-2.5 border rounded-lg bg-gray-50 dark:bg-gray-700 dark:text-white"
              required
              disabled={!isEditing}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 dark:text-white">
              Email
            </label>
            <input
              type="email"
              name="email"
              value={user.email}
              onChange={handleChange}
              className="w-full p-2.5 border rounded-lg bg-gray-50 dark:bg-gray-700 dark:text-white"
              required
              disabled={!isEditing}
            />
          </div>

          {isEditing && (
            <button
              type="submit"
              className="w-full text-white bg-blue-600 hover:bg-blue-700 p-2.5 rounded-lg"
            >
              Enregistrer
            </button>
          )}
        </form>

        <div className="mt-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Mot de passe
            </h2>
            {!isChangingPassword && (
              <button
                onClick={() => setIsChangingPassword(true)}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                Changer le mot de passe
              </button>
            )}
          </div>

          {isChangingPassword && (
            <form onSubmit={handleChangePassword} className="space-y-4 mt-4">
              <div>
  <label className="block text-sm font-medium text-gray-900 dark:text-white">
    Nouveau mot de passe
  </label>
  <div className="relative">
    <input
      type={showNewPassword ? "text" : "password"}
      name="new_password"
      value={passwords.new_password}
      onChange={handlePasswordChange}
      className="w-full p-2.5 border rounded-lg bg-gray-50 dark:bg-gray-700 dark:text-white"
      required
    />
    <button
      type="button"
      className="absolute inset-y-0 right-0 flex items-center pr-3"
      onClick={() => setShowNewPassword(!showNewPassword)}
    >
      {showNewPassword ? (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-500 dark:text-gray-400">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
        </svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-500 dark:text-gray-400">
          <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      )}
    </button>
  </div>
</div>

<div>
  <label className="block text-sm font-medium text-gray-900 dark:text-white">
    Confirmer le mot de passe
  </label>
  <div className="relative">
    <input
      type={showConfirmPassword ? "text" : "password"}
      name="confirm_password"
      value={passwords.confirm_password}
      onChange={handlePasswordChange}
      className="w-full p-2.5 border rounded-lg bg-gray-50 dark:bg-gray-700 dark:text-white"
      required
    />
    <button
      type="button"
      className="absolute inset-y-0 right-0 flex items-center pr-3"
      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
    >
      {showConfirmPassword ? (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-500 dark:text-gray-400">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
        </svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-500 dark:text-gray-400">
          <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      )}
    </button>
  </div>
</div>


              <button
                type="submit"
                className="w-full text-white bg-red-600 hover:bg-red-700 p-2.5 rounded-lg"
              >
                Enregistrer le nouveau mot de passe
              </button>
            </form>
          )}
        </div>

        <div className="mt-6">
          <button
            onClick={handleLogout}
            className="w-full px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-700"
          >
            Déconnexion
          </button>
        </div>
      </div>
    </div>
  );
}

export default Profile;