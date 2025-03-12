import React from "react";
import Header from "./Header";
import Footer from "./Footer";

function Accueil() {

  return (
    <>
      <main className="flex items-center justify-center min-h-screen  py-12 px-6">
        <div className="container mx-auto flex flex-col md:flex-row items-center gap-12">
          <div className="md:w-1/2 text-center md:text-left">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
              Bienvenue sur MMOTORS
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed">
              Votre destination premium pour découvrir les voitures d'exception.
              Explorez notre sélection exclusive de véhicules de luxe et de
              haute performance.
            </p>
          </div>
          <div className="md:w-1/2">
            <img
              src="/src/assets/voiture.png"
              alt="MMOTORS Luxury Car"
              className="w-4/5 h-auto mx-auto rounded-lg shadow-2xl transform hover:scale-105 transition-transform duration-300"
            />
          </div>
        </div>
      </main>
   
  <Footer/>
    </>
  );
}

export default Accueil;
