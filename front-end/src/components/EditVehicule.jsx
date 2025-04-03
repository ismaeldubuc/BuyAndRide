import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function EditVehicule() {
  const { id } = useParams();
  const [formData, setFormData] = useState({
    marque: "",
    modele: "",
    prix: "",
    kilometrage: "",
    energie: "",
    type: "",
    description: "",
  });
  const [images, setImages] = useState([]);
  const [existingPhotos, setExistingPhotos] = useState([]);

  // 🚗 Récupérer les données du véhicule
  useEffect(() => {
    const fetchVehicule = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/vehicules/${id}`);
        const data = await response.json();

        if (response.ok) {
          setFormData(data);
          setExistingPhotos(
            [
              data.photo1,
              data.photo2,
              data.photo3,
              data.photo4,
              data.photo5,
            ].filter(Boolean)
          );
        } else {
          console.error("Erreur lors de la récupération des données :", data);
        }
      } catch (error) {
        console.error("Erreur lors de la requête :", error);
      }
    };

    fetchVehicule();
  }, [id]);

  // 📝 Gérer les changements des champs
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 📸 Gérer l'ajout d'images
  const handleFileChange = (e) => {
    const files = Array.from(e.target.files).slice(0, 5 - images.length);
    setImages([...images, ...files]);
  };

  // 📨 Soumission du formulaire
  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();

    // Ajouter les données du formulaire
    Object.entries(formData).forEach(([key, value]) => {
      data.append(key, value);
    });

    // Ajouter les nouvelles images
    images.forEach((image, index) => {
      data.append(`photo${index + 1}`, image);
    });

    try {
      const response = await fetch(`http://127.0.0.1:5000/vehicules/${id}`, {
        method: "PUT",
        body: data,
        credentials: "include",
      });

      const result = await response.json();
      if (response.ok) {
        alert("Véhicule modifié avec succès !");
      } else {
        console.error("Erreur API:", result);
        alert(result.error || "Erreur inconnue");
      }
    } catch (error) {
      console.error("Erreur lors de l'envoi des données :", error);
      alert("Une erreur est survenue !");
    }
  };

  // 🚀 Interface du formulaire
  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col items-center justify-center w-full gap-5 p-5 mt-5"
    >
      {/* Zone d'upload d'images */}
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

      {/* Aperçu des images existantes */}
      <div className="flex flex-col gap-2 w-full">
        <h1>Images existantes :</h1>
        <div className="flex gap-2">
          {existingPhotos.map((photo, index) => (
            <img
              key={index}
              src={`http://127.0.0.1:5000/uploads/${photo}`}
              alt={`Photo ${index}`}
              className="w-24 h-24 object-cover rounded-lg border"
            />
          ))}
        </div>
      </div>

      {/* Aperçu des nouvelles images */}
      <div className="flex flex-col gap-2">
        <h1>Nouvelles images :</h1>
        <div className="flex gap-2">
          {images.map((image, index) => (
            <img
              key={index}
              src={URL.createObjectURL(image)}
              alt={`Aperçu ${index}`}
              className="w-24 h-24 object-cover rounded-lg border"
            />
          ))}
        </div>
      </div>

      {/* Champs du formulaire */}
      <div className="p-4 flex flex-col gap-4 w-full">
        {[
          { name: "marque", placeholder: "Marque" },
          { name: "modele", placeholder: "Modèle" },
          { name: "prix", placeholder: "Prix (€)" },
          { name: "kilometrage", placeholder: "Kilométrage (km)" },
          { name: "energie", placeholder: "Type d'énergie" },
          { name: "type", placeholder: "Type de véhicule" },
        ].map(({ name, placeholder }) => (
          <input
            key={name}
            type="text"
            name={name}
            placeholder={placeholder}
            value={formData[name] || ""}
            onChange={handleChange}
            className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
          />
        ))}

        <textarea
          name="description"
          placeholder="Description..."
          value={formData.description}
          onChange={handleChange}
          className="p-3 rounded-lg focus:outline-indigo-600 h-32 shadow-md border border-gray-300"
        ></textarea>
      </div>

      <button
        type="submit"
        className="bg-blue-500 text-white px-5 py-3 rounded-lg shadow-md hover:bg-green-600 transition"
      >
        Modifier
      </button>
    </form>
  );
}

export default EditVehicule;
