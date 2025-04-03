import { useState } from "react";
import Header from "./Header";
import { API_URL } from "../config";

function Annonce() {
  const [formData, setFormData] = useState({
    marque: "",
    modele: "",
    prix: "",
    km: "",
    energie: "",
    type: "",
    description: "",
  });

  const [images, setImages] = useState([]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files).slice(0, 5 - images.length);
    setImages([...images, ...files]);
  };

  const handleImageRemove = (indexToRemove) => {
    setImages(images.filter((_, index) => index !== indexToRemove));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Première requête pour envoyer les données du véhicule
      const vehiculeResponse = await fetch(`${API_URL}/vehicules`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(formData),
      });

      if (!vehiculeResponse.ok) {
        const errorData = await vehiculeResponse.json();
        throw new Error(
          errorData.error || "Erreur lors de la création du véhicule"
        );
      }

      const vehiculeResult = await vehiculeResponse.json();

      // Si des images sont présentes, les envoyer dans une seconde requête
      if (images.length > 0) {
        const imageData = new FormData();
        images.forEach((image, index) => {
          imageData.append(`photo${index + 1}`, image);
        });
        imageData.append("vehicule_id", vehiculeResult.id);

        const imageResponse = await fetch(`${API_URL}/upload-images`, {
          method: "POST",
          credentials: "include",
          body: imageData,
        });

        if (!imageResponse.ok) {
          const imageError = await imageResponse.json();
          throw new Error(
            imageError.error || "Erreur lors de l'upload des images"
          );
        }
      }

      alert("Véhicule ajouté avec succès !");
      // Réinitialiser le formulaire
      setFormData({
        marque: "",
        modele: "",
        prix: "",
        km: "",
        energie: "",
        type: "",
        description: "",
      });
      setImages([]);
    } catch (error) {
      console.error("Erreur lors de l'envoi des données :", error);
      alert(error.message || "Une erreur est survenue !");
    }
  };

  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center justify-center w-full gap-5 p-5 mt-5"
      >
        <label
          htmlFor="dropzone-file"
          className="flex flex-col items-center justify-center w-full h-48 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100"
        >
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            <p className="mb-2 text-sm text-gray-500">
              <span className="font-semibold">Cliquez pour télécharger</span> ou
              glissez-déposez
            </p>
            <p className="text-xs text-gray-500">JPG, PNG (MAX. 5 images)</p>
          </div>
          <input
            id="dropzone-file"
            type="file"
            className="hidden"
            accept="image/*"
            multiple
            onChange={handleFileChange}
          />
        </label>

        <div className="flex flex-col gap-2 w-full">
          <h1>Images téléchargées :</h1>
          <div className="flex flex-wrap gap-2">
            {images.map((image, index) => (
              <div key={index} className="relative">
                <img
                  src={
                    image instanceof File ? URL.createObjectURL(image) : image
                  }
                  alt={`Preview ${index + 1}`}
                  className="h-24 w-24 object-cover rounded-lg"
                  onError={(e) => {
                    console.error("Erreur de chargement de l'image:", image);
                    e.target.src = "/src/assets/placeholder.png";
                  }}
                />
                <button
                  type="button"
                  onClick={() => handleImageRemove(index)}
                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="p-4 flex flex-col gap-4 w-full">
          <div className="flex gap-4 items-center">
            <input
              type="text"
              name="marque"
              placeholder="Marque"
              value={formData.marque}
              onChange={handleChange}
              required
              className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3"
            />
            <input
              type="text"
              name="modele"
              placeholder="Modèle"
              value={formData.modele}
              onChange={handleChange}
              required
              className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
            />
          </div>
          <input
            type="number"
            name="prix"
            placeholder="Prix (€)"
            value={formData.prix}
            onChange={handleChange}
            required
            className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
          />
          <input
            type="number"
            name="km"
            placeholder="Kilométrage (km)"
            value={formData.km}
            onChange={handleChange}
            required
            className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
          />
          <select
            name="energie"
            value={formData.energie}
            onChange={handleChange}
            required
            className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
          >
            <option value="">Type d'énergie</option>
            <option value="Essence">Essence</option>
            <option value="Diesel">Diesel</option>
            <option value="Électrique">Électrique</option>
            <option value="Hybride">Hybride</option>
          </select>
          <select
            name="type"
            value={formData.type}
            onChange={handleChange}
            required
            className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
          >
            <option value="">Type d'annonce</option>
            <option value="true">Vente</option>
            <option value="false">Location</option>
          </select>
          <textarea
            name="description"
            placeholder="Description..."
            value={formData.description}
            onChange={handleChange}
            required
            className="p-3 rounded-lg focus:outline-indigo-600 h-96 shadow-md border border-gray-300"
          ></textarea>
        </div>

        <button
          type="submit"
          className="bg-[#24507F] text-white px-5 py-3 rounded-lg shadow-md hover:opacity-80 transition"
        >
          Poster l'annonce
        </button>
      </form>
    </>
  );
}

export default Annonce;
