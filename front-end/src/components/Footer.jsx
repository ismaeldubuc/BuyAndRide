import React from 'react'

function Footer() {
    const date = new Date().getFullYear();
    return (
        <footer className="bg-gray-800 text-white py-10 w-full mt-auto">
            <div className="container mx-auto px-6">
                <div className="flex flex-col items-center">
                    <div className="flex items-center mb-4">
                        <img
                            src="/src/assets/logo.svg"
                            alt="MMOTORS Logo"
                            className="h-12 w-auto mr-3 filter invert brightness-0"
                        />
                        <div className="text-3xl font-bold bg-gradient-to-r from-gray-300 to-gray-500 bg-clip-text text-transparent">
                            MMOTORS
                        </div>
                    </div>
                    <p className="text-gray-400 text-center">
                        ©{date} MMOTORS. Tous droits réservés.
                    </p>
                    <div className="mt-6 flex gap-4">
                        <a
                            href="#"
                            className="text-gray-400 hover:text-white transition-colors"
                        >
                            Mentions légales
                        </a>
                        <a
                            href="#"
                            className="text-gray-400 hover:text-white transition-colors"
                        >
                            Politique de confidentialité
                        </a>
                        <a
                            href="#"
                            className="text-gray-400 hover:text-white transition-colors"
                        >
                            Contact
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    )
}

export default Footer
