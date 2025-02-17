import React, { useState } from 'react';
import { Carousel } from 'react-responsive-carousel';
import "react-responsive-carousel/lib/styles/carousel.min.css";

const Acheter = () => {
    // Exemple de données (à remplacer par vos données de la BDD)
    const vehicules = [
        {
            id: 1,
            nom: "Mercedes Class A",
            prix: 25000,
            images: ["/img1.jpg", "/img2.jpg", "/img3.jpg"],
        },
        // ... autres véhicules
    ];

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8 text-center">Nos Véhicules à Vendre</h1>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {vehicules.map((vehicule) => (
                    <div key={vehicule.id} className="bg-white rounded-lg shadow-lg overflow-hidden">
                        <div className="flex flex-col md:flex-row">
                            {/* Carrousel d'images */}
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

                            {/* Informations du véhicule */}
                            <div className="w-full md:w-1/2 p-4">
                                <h2 className="text-xl font-semibold mb-2">{vehicule.nom}</h2>
                                <p className="text-2xl font-bold text-[#24507F] mb-4">
                                    {vehicule.prix.toLocaleString()} €
                                </p>
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
