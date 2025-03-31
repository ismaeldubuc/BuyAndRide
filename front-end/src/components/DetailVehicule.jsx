import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { API_URL, STATIC_URL } from '../config';
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

function DetailVehicule() {
  const { id } = useParams();
  const [vehicule, setVehicule] = useState(null);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
    const fetchVehicule = async () => {
      try {
        const response = await fetch(`${API_URL}/vehicules/${id}`, {
          credentials: 'include'
        });

        if (!response.ok) {
          throw new Error('Erreur lors de la récupération du véhicule');
        }

        const data = await response.json();
        setVehicule(data);
      } catch (error) {
        console.error('Erreur:', error);
        setErreur(error.message);
      }
    };

    fetchVehicule();
  }, [id]);

  const generatePDF = () => {
    const doc = new jsPDF();
    
    doc.setFont("helvetica", "bold");
    doc.setFontSize(20);
    doc.setTextColor(41, 128, 185);
    doc.text("BUY AND RIDE", 105, 15, { align: "center" });

    doc.setFontSize(16);
    doc.setTextColor(0, 0, 0);
    doc.text("Devis Véhicule", 105, 25, { align: "center" });
    
    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    doc.text(
        `Vendeur: ${vehicule.vendeur_prenom && vehicule.vendeur_nom ? 
            `${vehicule.vendeur_prenom} ${vehicule.vendeur_nom}` : 
            'M-Motors'}`,
        15,
        35
    );
    doc.text(`Date: ${new Date().toLocaleDateString()}`, 15, 42);

    autoTable(doc, {
        startY: 45,
        head: [["Caractéristiques", "Détails"]],
        body: [
            ["Marque", vehicule.marque],
            ["Modèle", vehicule.modele],
            ["Prix", `${vehicule.prix} ${vehicule.type ? '€' : '€/mois'}`],
            ["Kilométrage", `${vehicule.km} km`],
            ["Énergie", vehicule.energie],
            ["Type", vehicule.type ? 'À vendre' : 'À louer'],
        ],
        theme: "striped",
        headStyles: {
            fillColor: [41, 128, 185],
            textColor: [255, 255, 255],
            fontSize: 10,
            fontStyle: "bold",
        },
        bodyStyles: {
            fontSize: 10,
        },
        alternateRowStyles: {
            fillColor: [240, 240, 240],
        },
        margin: { left: 15, right: 15 },
    });

    doc.setFontSize(12);
    doc.setFont("helvetica", "bold");
    doc.text("Description du véhicule", 15, doc.lastAutoTable.finalY + 10);
    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    doc.text(vehicule.description, 15, doc.lastAutoTable.finalY + 20, {
        maxWidth: 180,
    });

    doc.setFontSize(12);
    doc.setFont("helvetica", "bold");
    doc.text("Conditions du devis", 15, doc.lastAutoTable.finalY + 50);

    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    const conditions = [
        "• Ce devis est valable 30 jours à compter de sa date d'émission",
        "• Prix indiqué hors frais d'immatriculation et de mise en route",
        "• Garantie selon conditions en vigueur",
        "• Photos non contractuelles",
    ];

    conditions.forEach((condition, index) => {
        doc.text(condition, 15, doc.lastAutoTable.finalY + 60 + (index * 7));
    });

    doc.text("Signature du vendeur:", 15, 250);
    doc.text("Signature de l'acheteur:", 120, 250);

    doc.setFontSize(8);
    doc.text("Buy And Ride - Tous droits réservés", 105, 280, {
        align: "center",
    });

    // Sauvegarder le PDF
    doc.save(`devis_${vehicule.marque}_${vehicule.modele}.pdf`);
  };

  if (erreur) return <div className="text-red-500">{erreur}</div>;
  if (!vehicule) return <div>Chargement...</div>;

  return (
    <div className="w-full px-8 mt-5">
      {/* Section principale avec images et infos de base */}
      <div className="row justify-content-between mb-5">
        {/* Galerie d'images */}
        <div className="col-8">
          <div className="carousel">
            {vehicule.photo1 && (
              <img 
                src={vehicule.photo1}
                alt={`${vehicule.marque} ${vehicule.modele}`}
                style={{ height: '600px', objectFit: 'cover' }}
                onError={(e) => {
                  console.error(`Erreur de chargement de l'image:`, vehicule.photo1);
                  e.target.src = '/src/assets/placeholder.png';
                }}
              />
            )}
            <div className="mt-2 d-flex gap-2">
              {[vehicule.photo2, vehicule.photo3, vehicule.photo4, vehicule.photo5]
                .filter(photo => photo)
                .map((photo, index) => (
                  <img
                    key={index}
                    src={photo}
                    alt={`Vue ${index + 2}`}
                    className="img-thumbnail"
                    style={{ width: '150px', height: '100px', objectFit: 'cover' }}
                    onError={(e) => {
                      console.error(`Erreur de chargement de l'image:`, photo);
                      e.target.src = '/src/assets/placeholder.png';
                    }}
                  />
                ))}
            </div>
          </div>
        </div>

        {/* Informations de base */}
        <div className="col-4">
          <div className="w-full bg-white rounded-lg shadow-lg p-8 space-y-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold">
                {vehicule.marque} {vehicule.modele}
              </h2>
            </div>
            <div className="space-y-4">
              <p className="text-lg">
                <span className="font-bold">Vendeur: </span>
                {vehicule.vendeur_prenom && vehicule.vendeur_nom ? 
                  `${vehicule.vendeur_prenom} ${vehicule.vendeur_nom}` : 
                  'M-Motors'}
              </p>
              <p className="text-lg">
                <span className="font-bold">Prix: </span>
                {vehicule.prix} {vehicule.type ? '€' : '€/mois'}
              </p>
              <p className="text-lg">
                <span className="font-bold">Kilométrage: </span>
                {vehicule.kilometrage} km
              </p>
              <p className="text-lg">
                <span className="font-bold">Énergie: </span>
                {vehicule.energie}
              </p>
              <p className="text-lg">
                <span className="font-bold">Type: </span>
                {vehicule.type ? 'À vendre' : 'À louer'}
              </p>
            </div>
            <div className="mt-6">
              <button
                onClick={generatePDF}
                className="w-full text-white bg-[#24507F] hover:opacity-80 focus:outline-none text-xl px-6 py-3 text-center rounded-lg"
              >
                Obtenir mon devis
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Section description détaillée */}
      <div className="row mt-4">
        <div className="col-12">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold mb-4">Description détaillée :</h3>
            <p className="text-gray-700">
              {vehicule.description}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DetailVehicule;
