import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { API_URL } from '../config';

function Header() {
  const [showMenu, setShowMenu] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch(`${API_URL}/check-login`, {
          credentials: 'include'
        });
        const data = await response.json();
        setIsConnected(data.isLoggedIn);
      } catch (error) {
        console.error('Erreur lors de la vérification de l\'authentification', error);
      }
    };

    checkAuth();
  }, []);

  const handleLogout = async () => {
    try {
      const response = await fetch(`${API_URL}/logout`, {
        method: "POST",
        credentials: "include",
      });

      if (response.ok) {
        setIsConnected(false);
        setShowMenu(false);
        navigate("/login-page");
      } else {
        console.error("Erreur lors de la déconnexion");
      }
    } catch (error) {
      console.error("Erreur lors de la déconnexion:", error);
    }
  };

  return (
    <header className="bg-white dark:bg-gray-900 shadow-md w-full font-['Plus_Jakarta_Sans']">
      <div className="flex justify-between items-center w-full px-4 py-3">
        <div className="flex items-center">
          <img src="/src/assets/logo.svg" alt="Logo" className="w-20 h-20" onClick={() => navigate("/")}/>
        </div>

        <div className="flex space-x-40">
          <button className="text-[#24507F] hover:opacity-80 text-3xl px-4 py-2 transition"
          onClick={() => navigate("/acheter-page")}
          >
            Acheter
          </button>
          <button className="text-[#508DCE] hover:opacity-80 text-3xl px-4 py-2 transition"
            onClick={() => navigate("/louer-page")}
          >
            Louer
          </button>
          <button className="text-[#90B6E0] hover:opacity-80 text-3xl px-4 py-2 transition"
            onClick={() => navigate("/addVehicule")}
          >
            Vendre
          </button>
        </div>
        <div className="relative">
          <button
            className="focus:outline-none"
            onClick={() => setShowMenu(!showMenu)}
          >
            <svg
              className="w-10 h-10 text-[#508DCE]"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z" />
            </svg>
          </button>

          {showMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg py-2 shadow-lg z-50">
              {isConnected ? (
                <>
                  <button
                    className="w-full px-4 py-2 text-left text-[#24507F] hover:bg-gray-100 transition"
                    onClick={() => navigate("/profile-page")}
                  >
                    Profil
                  </button>
                  <button
                    className="w-full px-4 py-2 text-left text-[#24507F] hover:bg-gray-100 transition"
                    onClick={handleLogout}
                  >
                    Déconnexion
                  </button>
                </>
              ) : (
                <>
                  <button
                    className="w-full px-4 py-2 text-left text-[#24507F] hover:bg-gray-100 transition"
                    onClick={() => navigate("/login-page")}
                  >
                    Connexion
                  </button>
                  <button
                    className="w-full px-4 py-2 text-left text-[#24507F] hover:bg-gray-100 transition"
                    onClick={() => navigate("/register-page")}
                  >
                    Inscription
                  </button>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;
