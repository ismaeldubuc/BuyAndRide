import { useState } from "react";

function Annonce() {
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

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files).slice(0, 5 - images.length);
    setImages([...images, ...files]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      data.append(key, value);
    });

    images.forEach((image, index) => {
      data.append(`photo${index + 1}`, image);
    });

    try {
      const response = await fetch("http://127.0.0.1:5000/vehicules", {
        method: "POST",
        body: data,
        credentials: "include", // Indispensable pour envoyer les cookies de session
      });

      const result = await response.json();

      if (response.ok) {
        alert("Véhicule ajouté avec succès !");
        setFormData({
          marque: "",
          modele: "",
          prix: "",
          kilometrage: "",
          energie: "",
          type: "",
          description: "",
        });
        setImages([]);
      } else {
        console.error("Erreur API:", result);
        alert(result.error || "Erreur inconnue");
      }
    } catch (error) {
      console.error("Erreur lors de l'envoi des données :", error);
      alert("Une erreur est survenue !");
    }
  };

  return (
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
      <div className="flex flex-col gap-2">
        <h1>Images téléchargées :</h1>
        <div className="flex">
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

      <div className="p-4 flex flex-col gap-4 w-full">
        <div className="flex gap-4 items-center">
          <select
            name="marque"
            value={formData.marque}
            onChange={handleChange}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3"
          >
            <option value="">Choisissez une marque</option>
            <option value="BMW">BMW</option>
            <option value="DACIA">DACIA</option>
            <option value="TOYOTA">TOYOTA</option>
            <option value="MITSUBISHI MOTORS">MITSUBISHI MOTORS</option>
          </select>
          <input
            type="text"
            name="modele"
            placeholder="Modèle"
            value={formData.modele}
            onChange={handleChange}
            className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border  border-gray-300"
          />
        </div>
        <input
          type="number"
          name="prix"
          placeholder="Prix (€)"
          value={formData.prix}
          onChange={handleChange}
          className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
        />
        <input
          type="text"
          name="kilometrage"
          placeholder="Kilométrage (km)"
          value={formData.kilometrage}
          onChange={handleChange}
          className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
        />
        <input
          type="text"
          name="energie"
          placeholder="Type d'énergie"
          value={formData.energie}
          onChange={handleChange}
          className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
        />
        <input
          type="text"
          name="type"
          placeholder="Type de véhicule"
          value={formData.type}
          onChange={handleChange}
          className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
        />
        <textarea
          name="description"
          placeholder="Description..."
          value={formData.description}
          onChange={handleChange}
          className="p-3 rounded-lg focus:outline-indigo-600 h-96 shadow-md border border-gray-300"
        ></textarea>
      </div>

      <button
        type="submit"
        className="bg-blue-500 text-white px-5 py-3 rounded-lg shadow-md hover:bg-blue-600 transition"
      >
        Poster
      </button>
    </form>
  );
}

export default Annonce;
