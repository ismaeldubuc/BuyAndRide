import { useState } from 'react';

function Header() {
    const [showMenu, setShowMenu] = useState(false);

    return (
        <header className="bg-white dark:bg-gray-900 shadow-md w-full font-['Plus_Jakarta_Sans']">
            <div className="flex justify-between items-center w-full px-4">
                {/* Logo à gauche */}
                <div className="flex items-center">
                    <img src="/src/assets/logo.svg" alt="Logo" className="w-20 h-20" />
                </div>

                {/* Boutons au centre */}
                <div className="flex space-x-40">
                    <button className="text-[#24507F] hover:opacity-80 focus:outline-none text-3xl px-4 py-2 text-center transition duration-300 font-['Plus_Jakarta_Sans']">
                        Acheter
                    </button>
                    <button className="text-[#508DCE] hover:opacity-80 focus:outline-none text-3xl px-4 py-2 text-center transition duration-300 font-['Plus_Jakarta_Sans']">
                        Louer
                    </button>
                    <button className="text-[#90B6E0] hover:opacity-80 focus:outline-none text-3xl px-4 py-2 text-center transition duration-300 font-['Plus_Jakarta_Sans']">
                        Vendre
                    </button>
                </div>

                {/* Icône de profil à droite avec menu déroulant */}
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
                            <path 
                                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"
                            />
                        </svg>
                    </button>

                    {/* Menu déroulant */}
                    {showMenu && (
                        <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg py-2 z-50 shadow-[0_0_10px_rgba(0,0,0,0.2)]">
                            <button 
                                className="w-full px-4 py-2 text-left text-[#24507F] hover:bg-gray-100 transition duration-300"
                            >
                                Profil
                            </button>
                            <button 
                                className="w-full px-4 py-2 text-left text-[#24507F] hover:bg-gray-100 transition duration-300"
                            >
                                Déconnexion
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}

export default Header;
