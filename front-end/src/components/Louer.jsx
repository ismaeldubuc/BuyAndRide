import React, { useState, useEffect } from "react";
import { Carousel } from "react-responsive-carousel";
import "react-responsive-carousel/lib/styles/carousel.min.css";
import { BiSolidCarMechanic, BiGasPump } from "react-icons/bi";
import { TbWheel } from "react-icons/tb";
import { BiEuro } from "react-icons/bi";
import { useNavigate } from "react-router-dom";
import { API_URL } from "../config";
import axios from "axios";
import { Link } from "react-router-dom";

const Louer = () => {
  const [filtres, setFiltres] = useState({
    marque: "",
    modele: "",
    prix: "",
    km: "",
    energie: "",
    type: "",
  });
  const [vehicules, setVehicules] = useState([]);
  const [marques, setMarques] = useState([]);
  const [modeles, setModeles] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const chargerVehicules = async () => {
      try {
        const response = await fetch(`${API_URL}/get-louer-vehicule`, {
          credentials: "include",
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(
            errorData.message || "Erreur lors de la récupération des véhicules"
          );
        }

        const data = await response.json();
        console.log("Données reçues:", data); // Pour le débogage

        if (!Array.isArray(data)) {
          console.error("Format de données invalide:", data);
          throw new Error("Format de données invalide");
        }

        const vehiculesTransformes = data.map((vehicule) => ({
          id: vehicule.id,
          nom: `${vehicule.marque} ${vehicule.modele}`,
          modele: vehicule.modele,
          marque: vehicule.marque,
          energie: vehicule.energie,
          km: vehicule.km || 0,
          prix: parseFloat(vehicule.prix || 0),
          images: [
            vehicule.photo1,
            vehicule.photo2,
            vehicule.photo3,
            vehicule.photo4,
            vehicule.photo5,
          ].filter(Boolean), // Filtrer les valeurs null/undefined
        }));

        setVehicules(vehiculesTransformes);

        const marquesUniques = [...new Set(data.map((v) => v.marque))];
        setMarques(marquesUniques);
        setError(null);
      } catch (error) {
        console.error("Erreur lors du chargement des véhicules:", error);
        setVehicules([]);
        setMarques([]);
        setError(error.message);
      }
    };

    chargerVehicules();
  }, []);

  // Mettre à jour les modèles quand une marque est sélectionnée
  const handleFiltreChange = (e) => {
    const { name, value } = e.target;
    setFiltres((prev) => ({ ...prev, [name]: value }));

    if (name === "marque") {
      // Filtrer les modèles pour la marque sélectionnée
      const modelesUniques = [
        ...new Set(
          vehicules.filter((v) => v.marque === value).map((v) => v.modele)
        ),
      ];
      setModeles(modelesUniques);
      setFiltres((prev) => ({ ...prev, modele: "" })); // Réinitialiser le modèle
    }
  };

  const appliquerFiltres = async () => {
    const params = new URLSearchParams();

    // Ajouter type=false pour la page Louer
    params.append("type", "false");

    // Ajouter les autres filtres
    Object.entries(filtres).forEach(([key, value]) => {
      if (value && key !== "type") {
        // Exclure le type car déjà ajouté
        params.append(key, value);
      }
    });

    try {
      const response = await fetch(`${API_URL}/filter-vehicles?${params}`, {
        method: "GET",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la récupération des véhicules");
      }

      const data = await response.json();
      const vehiculesTransformes = data.map((vehicule) => ({
        id: vehicule.id,
        nom: `${vehicule.marque} ${vehicule.modele}`,
        modele: vehicule.modele,
        marque: vehicule.marque,
        energie: vehicule.energie,
        km: vehicule.km,
        prix: parseFloat(vehicule.prix),
        images: [
          vehicule.photo1,
          vehicule.photo2,
          vehicule.photo3,
          vehicule.photo4,
          vehicule.photo5,
        ].filter((photo) => photo),
      }));
      setVehicules(vehiculesTransformes);
    } catch (error) {
      console.error("Erreur:", error);
      alert("Erreur lors de la recherche des véhicules");
    }
  };

  const naviguerVersDetails = (vehiculeId) => {
    navigate(`/vehicules/${vehiculeId}`);
  };

  if (error) {
    return <div className="text-red-500 text-center p-4">{error}</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">
        Nos Véhicules à Louer
      </h1>

      <div className="mb-8 bg-white p-4 rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold mb-4">Filtres</h2>
        <div className="flex flex-row gap-4 overflow-x-auto items-center">
          <select
            name="marque"
            value={filtres.marque}
            onChange={handleFiltreChange}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-48 p-3 flex-shrink-0"
          >
            <option value="">Toutes les marques</option>
            {marques.map((marque) => (
              <option key={marque} value={marque}>
                {marque}
              </option>
            ))}
          </select>

          <select
            name="modele"
            value={filtres.modele}
            onChange={handleFiltreChange}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-48 p-3 flex-shrink-0"
            disabled={!filtres.marque}
          >
            <option value="">Tous les modèles</option>
            {modeles.map((modele) => (
              <option key={modele} value={modele}>
                {modele}
              </option>
            ))}
          </select>

          <select
            name="energie"
            value={filtres.energie}
            onChange={handleFiltreChange}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-48 p-3 flex-shrink-0"
          >
            <option value="">Type d'énergie</option>
            <option value="Essence">Essence</option>
            <option value="Diesel">Diesel</option>
            <option value="Électrique">Électrique</option>
            <option value="Hybride">Hybride</option>
          </select>

          <input
            type="number"
            name="prix"
            placeholder="Prix maximum (€)"
            value={filtres.prix}
            onChange={handleFiltreChange}
            className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300 w-48 flex-shrink-0"
          />

          <input
            type="number"
            name="km"
            placeholder="Kilométrage maximum"
            value={filtres.km}
            onChange={handleFiltreChange}
            className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300 w-48 flex-shrink-0"
          />

          <button
            onClick={appliquerFiltres}
            className="bg-[#24507F] text-white py-3 px-6 rounded-lg hover:opacity-80 transition duration-300 flex-shrink-0 h-[46px]"
          >
            Filtrer
          </button>
        </div>
      </div>

      {vehicules.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {vehicules.map((vehicule) => (
            <div
              key={vehicule.id}
              className="bg-white rounded-lg shadow-lg overflow-hidden"
            >
              <div className="flex flex-col md:flex-row">
                <div className="w-full md:w-1/2">
                  <Carousel
                    showThumbs={false}
                    showStatus={false}
                    infiniteLoop={true}
                    className="h-full"
                  >
                    {vehicule.images.map((image, index) => (
                      <div key={index} className="h-64">
                        <img
                          src={image}
                          alt={`${vehicule.nom} - Image ${index + 1}`}
                          className="object-cover w-full h-full"
                        />
                      </div>
                    ))}
                  </Carousel>
                </div>

                <div className="w-full md:w-1/2 p-4">
                  <h2 className="text-2xl font-bold mb-4">{vehicule.nom}</h2>
                  <div className="space-y-3">
                    <div className="flex items-center">
                      <span className="font-semibold w-16">
                        <BiSolidCarMechanic className="text-xl" />
                      </span>
                      <span>{vehicule.modele}</span>
                    </div>
                    <div className="flex items-center">
                      <span className="font-semibold w-16">
                        <BiGasPump className="text-xl" />
                      </span>
                      <span>{vehicule.energie}</span>
                    </div>
                    <div className="flex items-center">
                      <span className="font-semibold w-16">
                        <TbWheel className="text-xl" />
                      </span>
                      <span>{vehicule.km.toLocaleString()} km</span>
                    </div>
                    <div className="flex items-center">
                      <span className="font-semibold w-16">
                        <BiEuro className="text-xl" />
                      </span>
                      <span>{vehicule.prix.toLocaleString()} €/mois</span>
                    </div>
                  </div>
                  <button
                    className="w-full bg-[#24507F] text-white py-2 px-4 rounded-lg hover:opacity-80 transition duration-300"
                    onClick={() => naviguerVersDetails(vehicule.id)}
                  >
                    Voir plus de détails
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Aucun véhicule ne correspond à vos critères
            </h2>
            <p className="text-gray-600 mb-4">
              Nous sommes désolés, mais aucune annonce ne correspond
              actuellement à vos critères de recherche. Nous vous suggérons de :
            </p>
            <ul className="text-gray-600 text-left list-disc pl-6 mb-6">
              <li>Élargir votre recherche en modifiant vos filtres</li>
              <li>Vérifier régulièrement les nouvelles annonces</li>
              <li>Essayer avec des critères moins restrictifs</li>
            </ul>
            <button
              onClick={() => {
                setFiltres({
                  marque: "",
                  modele: "",
                  prix: "",
                  km: "",
                  energie: "",
                  type: "",
                });
                appliquerFiltres();
              }}
              className="bg-[#24507F] text-white py-2 px-6 rounded-lg hover:opacity-80 transition duration-300"
            >
              Réinitialiser les filtres
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Louer;
