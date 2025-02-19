// BuyAndRide/front-end/src/components/VehicleDetails.jsx
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FaCar } from "react-icons/fa6";
import { BiSolidCarMechanic, BiGasPump } from 'react-icons/bi';
import { TbWheel } from "react-icons/tb";
import { BiEuro } from "react-icons/bi";
import { useLocation, useParams } from 'react-router-dom';


const VehicleDetails = () => {
    const { id } = useParams();
    const location = useLocation();
    const vehiculeId = location.state?.vehiculeId;

    // Vous pouvez maintenant utiliser l'id pour charger les détails du véhicule
    console.log("ID du véhicule:", id);

    const images = [
        "https://wallpaperaccess.com/full/16270709.jpg",
        "https://wallpaperaccess.com/full/7013653.jpg",
        "https://wallpaperaccess.com/full/970693.jpg",
        "https://wallpaperaccess.com/full/16270709.jpg",
        "https://wallpaperaccess.com/full/7013653.jpg"
    ];

    const [currentIndex, setCurrentIndex] = useState(0);

    const handlePrevClick = () => {
        setCurrentIndex((prevIndex) => (prevIndex === 0 ? images.length - 1 : prevIndex - 1));
    };

    const handleNextClick = () => {
        setCurrentIndex((prevIndex) => (prevIndex === images.length - 1 ? 0 : prevIndex + 1));
    };

    const handleThumbnailClick = (index) => {
        setCurrentIndex(index);
    };

    return (
        <div className="w-full px-8 mt-5">
            {/* Section principale avec images et infos de base */}
            <div className="row justify-content-between mb-5">
                {/* Galerie de miniatures à gauche */}
                <div className="col-1">
                    <div className="d-flex flex-column gap-2 justify-content-between" style={{ height: '600px' }}>
                        {images.map((image, index) => (
                            <img
                                key={index}
                                src={image}
                                alt={`Thumbnail ${index + 1}`}
                                className={`img-thumbnail ${index === currentIndex ? 'border-primary border-2' : ''}`}
                                style={{ 
                                    width: '100%', 
                                    height: '80px',
                                    objectFit: 'cover', 
                                    cursor: 'pointer',
                                    opacity: index === currentIndex ? 1 : 0.6
                                }}
                                onClick={() => handleThumbnailClick(index)}
                            />
                        ))}
                    </div>
                </div>

                {/* Image principale au milieu */}
                <div className="col-7">
                    <div className="carousel">
                        <img 
                            src={images[currentIndex]} 
                            className="d-block w-100" 
                            alt={`Image ${currentIndex + 1}`}
                            style={{ height: '600px', objectFit: 'cover' }}
                        />
                        <button className="carousel-control-prev" onClick={handlePrevClick}>
                            <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span className="sr-only">Précédent</span>
                        </button>
                        <button className="carousel-control-next" onClick={handleNextClick}>
                            <span className="carousel-control-next-icon" aria-hidden="true"></span>
                            <span className="sr-only">Suivant</span>
                        </button>
                    </div>
                </div>

                {/* Informations de base à droite */}
                <div className="col-4">
                    <div className="w-full bg-white rounded-lg shadow-lg p-8 space-y-6 md:space-y-8 text-black" style={{ height: '600px', display: 'flex', flexDirection: 'column' }}>
                        <div className="mb-6">
                            <h2 className="text-2xl font-bold leading-tight tracking-tight md:text-3xl">
                                Description de la Voiture
                            </h2>
                        </div>
                        <div className="grid grid-cols-1 gap-12" style={{ flex: 1 }}>
                            <div className="space-y-12">
                                <div className="d-flex justify-content-between">
                                    <p className="text-lg d-flex align-items-center gap-2">
                                        <FaCar className="text-xl" />
                                        <span className="font-bold">Marque: </span> 
                                        <span className="font-normal">Exemple</span>
                                    </p>
                                    <p className="text-lg d-flex align-items-center gap-2">
                                        <BiSolidCarMechanic className="text-xl" />
                                        <span className="font-bold">Modèle: </span> 
                                        <span className="font-normal">Exemple</span>
                                    </p>
                                </div>

                                <div className="d-flex justify-content-between">
                                    <p className="text-lg d-flex align-items-center gap-2">
                                        <BiGasPump className="text-xl" />
                                        <span className="font-bold">Énergie: </span> 
                                        <span className="font-normal">énergie</span>
                                    </p>
                                    <p className="text-lg d-flex align-items-center gap-2">
                                        <TbWheel className="text-xl" />
                                        <span className="font-bold">Kilométrage : </span> 
                                        <span className="font-normal">15000</span>
                                    </p>
                                </div>

                                <p className="text-lg d-flex align-items-center gap-2">
                                    <BiEuro className="text-xl" />
                                    <span className="font-bold">Prix:</span> 
                                    <span className="font-normal">20,000€</span>
                                </p>
                            </div>
                            <div className="mt-auto">
                                <button
                                    type="submit"
                                    className="w-full text-white bg-[#24507F] hover:opacity-80 focus:outline-none text-3xl px-6 py-4 text-center transition duration-300 font-['Plus_Jakarta_Sans'] border-2 border-[#24507F] rounded-lg shadow-lg hover:shadow-xl"
                                >
                                    Obtenir mon devis
                                </button>
                                <p className="text-sm text-gray-600 mt-4 text-center px-2">
                                    En cliquant sur le bouton "Obtenir mon devis", un devis sera généré et l'un de nos commerciaux en sera averti. Il vous recontactera ensuite.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Section description détaillée en dessous */}
            <div className="row mt-4">
                <div className="col-12">
                    <div>
                        <h3 className="text-xl font-bold mb-4">Description détaillée :</h3>
                        <span className="font-normal">
                            Cette voiture est un excellent choix pour ceux qui recherchent une conduite confortable et économique.
                        </span>
                        
                    </div>
                </div>
            </div>
        </div>
    );
};

export default VehicleDetails;