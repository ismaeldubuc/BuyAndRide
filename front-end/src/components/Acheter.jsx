import React, { useState, useEffect } from 'react';
import { Carousel } from 'react-responsive-carousel';
import "react-responsive-carousel/lib/styles/carousel.min.css";
import { BiSolidCarMechanic, BiGasPump } from 'react-icons/bi';
import { TbWheel } from "react-icons/tb";
import { BiEuro } from "react-icons/bi";

const Acheter = () => {
    const [filtres, setFiltres] = useState({
        marque: "",
        modele: "",
        prix: "",
        kilometrage: "",
        energie: "",
        type: ""
    });
    const [vehicules, setVehicules] = useState([]);
    const [marques, setMarques] = useState([]);
    const [modeles, setModeles] = useState([]);

    const handleFiltreChange = (e) => {
        const { name, value } = e.target;
        setFiltres(prev => ({ ...prev, [name]: value }));
        
        if (name === 'marque') {
            chargerModeles(value);
            setFiltres(prev => ({ ...prev, modele: '' }));
        }
    };

    const appliquerFiltres = async () => {
        const params = new URLSearchParams();
        Object.entries(filtres).forEach(([key, value]) => {
            if (value) {
                params.append(key, value);
            }
        });

        try {
            const response = await fetch(`http://127.0.0.1:5000/vehicules/filter?${params}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Erreur lors de la récupération des véhicules');
            }

            const data = await response.json();
            setVehicules(data);
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la recherche des véhicules');
        }
    };

    const chargerMarques = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/marques', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Erreur lors du chargement des marques');
            }

            const data = await response.json();
            setMarques(data);
        } catch (error) {
            console.error('Erreur:', error);
        }
    };

    const chargerModeles = async (marqueSelectionnee) => {
        if (!marqueSelectionnee) {
            setModeles([]);
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:5000/modeles/${marqueSelectionnee}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Erreur lors du chargement des modèles');
            }

            const data = await response.json();
            setModeles(data);
        } catch (error) {
            console.error('Erreur:', error);
        }
    };

    useEffect(() => {
        const chargerVehicules = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/vehicules', {
                    credentials: 'include'
                });
                if (response.ok) {
                    const data = await response.json();
                    setVehicules(data);
                }
            } catch (error) {
                console.error('Erreur lors du chargement des véhicules:', error);
            }
        };

        chargerMarques();
        chargerVehicules();
    }, []);

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8 text-center">Nos Véhicules à Vendre</h1>
            
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
                            <option key={marque} value={marque}>{marque}</option>
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
                            <option key={modele} value={modele}>{modele}</option>
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
                        name="kilometrage"
                        placeholder="Kilométrage maximum"
                        value={filtres.kilometrage}
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

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {vehicules.map((vehicule) => (
                    <div key={vehicule.id} className="bg-white rounded-lg shadow-lg overflow-hidden">
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
                                        <span className="font-semibold w-16"><BiSolidCarMechanic className="text-xl" /></span>
                                        <span>{vehicule.modele}</span>
                                    </div>
                                    <div className="flex items-center">
                                        <span className="font-semibold w-16"><BiGasPump className="text-xl" /></span>
                                        <span>{vehicule.energie}</span>
                                    </div>
                                    <div className="flex items-center">
                                        <span className="font-semibold w-16"><TbWheel className="text-xl" /></span>
                                        <span>{vehicule.kilometrage.toLocaleString()} km</span>
                                    </div>
                                    <div className="flex items-center">
                                        <span className="font-semibold w-16"><BiEuro className="text-xl" /></span>
                                        <span>{vehicule.prix.toLocaleString()} €</span>
                                    </div>
                                </div>
                                <button
                                    className="w-full bg-[#24507F] text-white py-2 px-4 rounded-lg hover:opacity-80 transition duration-300"
                                    onClick={() => {/* Navigation vers la page détaillée */}}
                                >
                                    Voir plus de détails
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Acheter;
