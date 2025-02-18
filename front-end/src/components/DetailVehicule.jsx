import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export default function DetailVehicule() {
  const { id } = useParams();
  const [vehicule, setVehicule] = useState(null);

  const [erreur, setErreur] = useState(null); 
  useEffect(() => {
    const fetchVehicule = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/vehicules/${id}`
        );
        console.log("Données reçues:", response.data);
        setVehicule(response.data);
        setErreur(null); 
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.error("Erreur Axios:", error.message);
          setErreur(error.message);
        } else {
          console.error("Erreur inconnue:", error);
          setErreur("Erreur inconnue");
        }
        setVehicule(null); 
      }
    };
    fetchVehicule();
  }, [id]);



const generatePDF = () => {
    const doc = new jsPDF();
    doc.setFont("helvetica", "bold");
    doc.setFontSize(18);
    doc.text("Détails du véhicule", 105, 15, { align: "center" });
  
    
    autoTable(doc, {
      startY: 25,
      head: [["Champ", "Valeur"]],
      body: [
        ["Marque", vehicule.marque],
        ["Modèle", vehicule.modele],
        ["Prix (€)", vehicule.prix],
        ["Kilométrage (km)", vehicule.kilometrage],
        ["Type d'énergie", vehicule.energie],
        ["Type", vehicule.type],
      ],
      theme: "striped",
      headStyles: { fillColor: [41, 128, 185] },
    });
  

    doc.setFontSize(14);
    doc.text("Description :", 15, doc.lastAutoTable.finalY + 10);
    doc.setFontSize(12);
    doc.text(vehicule.description, 15, doc.lastAutoTable.finalY + 20, {
      maxWidth: 180,
    });
  
    let yPosition = doc.lastAutoTable.finalY + 40;
  
   
    const promises = [];
    const images = [
      `http://localhost:8000/static/${vehicule.photo1}`,
      `http://localhost:8000/static/${vehicule.photo2}`,
      `http://localhost:8000/static/${vehicule.photo3}`,
      `http://localhost:8000/static/${vehicule.photo4}`,
      `http://localhost:8000/static/${vehicule.photo5}`,
    ];
  
    images.forEach((image, index) => {
      if (image) {
        promises.push(
          new Promise((resolve) => { 
            const img = new Image();
            img.crossOrigin = "Anonymous";
            img.onload = () => {
              console.log(`Image ${index + 1} chargée avec succès`);
              if (yPosition > 260) {
                doc.addPage();
                yPosition = 20;
              }
              doc.addImage(img, "JPEG", 15, yPosition, 60, 40);
              yPosition += 50;
              resolve({ status: 'fulfilled', value: img }); 
            };
            img.onerror = () => {
              console.error(`Erreur de chargement de l'image ${index + 1}`);
              resolve({ status: 'rejected', reason: `Erreur de chargement de l'image ${index + 1}` });
            };
            img.src = image;
          })
        );
      }
    });
  
 
    Promise.allSettled(promises) 
      .then((results) => {
        console.log("Toutes les promesses sont réglées :", results);
        results.forEach((result, index) => {
          if (result.status === 'fulfilled' && result.value) {
            
          } else {
            console.error(`Image ${index + 1} n'a pas pu être chargée :`, result.reason);
          }
        });
        doc.save(`voiture_details.pdf`); 
      });
  };
  
  if (!vehicule) return <div>Chargement...</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">
        {vehicule.marque} {vehicule.modele}
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <img
            src={`http://localhost:8000/static/${vehicule.photo1}`}
            alt={`${vehicule.marque} ${vehicule.modele}`}
            className="w-full rounded-lg"
          />
          <div className="grid grid-cols-4 gap-2 mt-2">
            {[2, 3, 4, 5].map(
              (num) =>
                vehicule[`photo${num}`] && (
                  <img
                    key={num}
                    src={`http://localhost:8000/static/${
                      vehicule[`photo${num}`]
                    }`}
                    alt={`Vue ${num}`}
                    className="w-full h-20 object-cover rounded"
                  />
                )
            )}
          </div>
        </div>
        <div>
          <p className="text-2xl font-bold">{vehicule.prix} €</p>
          <p className="text-gray-600">{vehicule.kilometrage} km</p>
          <p className="text-gray-600">{vehicule.energie}</p>
          <p className="text-gray-600">{vehicule.type}</p>
          <p className="text-gray-600">{vehicule.description}</p>
          <div className="mt-6">
            <button
              onClick={generatePDF}
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            >
              Télécharger le devis
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
