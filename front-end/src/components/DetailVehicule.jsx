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
    doc.setFontSize(24);
    doc.setTextColor(41, 128, 185);
    doc.text("BUY AND RIDE", 105, 15, { align: "center" });

    doc.setFontSize(18);
    doc.setTextColor(0, 0, 0);
    doc.text("Devis Véhicule", 105, 30, { align: "center" });

    doc.setFontSize(12);
    doc.setFont("helvetica", "normal");
    doc.text(
      `Vendeur: ${vehicule.vendeur_prenom} ${vehicule.vendeur_nom}`,
      15,
      45
    );
    doc.text(`Date: ${new Date().toLocaleDateString()}`, 15, 52);

    autoTable(doc, {
      startY: 60,
      head: [["Caractéristiques", "Détails"]],
      body: [
        ["Marque", vehicule.marque],
        ["Modèle", vehicule.modele],
        ["Prix", `${vehicule.prix} €`],
        ["Kilométrage", `${vehicule.kilometrage} km`],
        ["Énergie", vehicule.energie],
        ["Type", vehicule.type],
      ],
      theme: "striped",
      headStyles: {
        fillColor: [41, 128, 185],
        textColor: [255, 255, 255],
        fontSize: 12,
        fontStyle: "bold",
      },
      bodyStyles: {
        fontSize: 11,
      },
      alternateRowStyles: {
        fillColor: [240, 240, 240],
      },
    });

    doc.setFontSize(14);
    doc.setFont("helvetica", "bold");
    doc.text("Description du véhicule", 15, doc.lastAutoTable.finalY + 20);
    doc.setFontSize(11);
    doc.setFont("helvetica", "normal");
    doc.text(vehicule.description, 15, doc.lastAutoTable.finalY + 30, {
      maxWidth: 180,
    });

    let yPosition = doc.lastAutoTable.finalY + 60;
    const promises = [];
    const images = [
      vehicule.photo1,
      vehicule.photo2,
      vehicule.photo3,
      vehicule.photo4,
      vehicule.photo5,
    ].filter(Boolean);

    images.forEach((photo, index) => {
      if (photo) {
        promises.push(
          new Promise((resolve) => {
            const img = new Image();
            img.crossOrigin = "Anonymous";
            img.onload = () => {
              if (yPosition > 250) {
                doc.addPage();
                yPosition = 20;
              }
              doc.addImage(img, "JPEG", 15, yPosition, 80, 60);
              yPosition += 70;
              resolve();
            };
            img.src = `http://localhost:8000/static/${photo}`;
          })
        );
      }
    });

    Promise.all(promises).then(() => {
      doc.addPage();
      doc.setFontSize(14);
      doc.setFont("helvetica", "bold");
      doc.text("Conditions du devis", 105, 20, { align: "center" });

      doc.setFontSize(11);
      doc.setFont("helvetica", "normal");
      const conditions = [
        "• Ce devis est valable 30 jours à compter de sa date d'émission",
        "• Prix indiqué hors frais d'immatriculation et de mise en route",
        "• Garantie selon conditions en vigueur",
        "• Photos non contractuelles",
      ];

      conditions.forEach((condition, index) => {
        doc.text(condition, 15, 40 + index * 10);
      });

      doc.text("Signature du vendeur:", 15, 230);
      doc.text("Signature de l'acheteur:", 120, 230);

      doc.setFontSize(8);
      doc.text("Buy And Ride - Tous droits réservés", 105, 280, {
        align: "center",
      });

      const pdfOutput = doc.output("arraybuffer");

      fetch(`http://localhost:8000/api/devis/${vehicule.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/pdf",
        },
        body: pdfOutput,
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("PDF sauvegardé:", data);
          doc.save(`devis_${vehicule.marque}_${vehicule.modele}.pdf`);
        })
        .catch((error) => {
          console.error("Erreur:", error);
        });
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
