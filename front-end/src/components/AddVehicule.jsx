import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { XCircleIcon } from "@heroicons/react/solid";

export default function AddVehicule() {
  const navigate = useNavigate();
  const [showSuccess, setShowSuccess] = useState(false);
  const [photoCount, setPhotoCount] = useState(0);
  const [formData, setFormData] = useState({
    marque: "",
    modele: "",
    prix: "",
    kilometrage: "",
    energie: "",
    type: "",
    description: "",
    photos: [],
  });

  const handlePhotoChange = (e) => {
    const files = Array.from(e.target.files);

    if (files.length + formData.photos.length > 5) {
      alert(
        `Vous pouvez ajouter jusqu'à 5 photos. Il reste ${
          5 - formData.photos.length
        } emplacement(s).`
      );
      return;
    }

    setFormData((prevData) => ({
      ...prevData,
      photos: [...prevData.photos, ...files],
    }));

    setPhotoCount(formData.photos.length + files.length);
  };

  const handleRemovePhoto = (index) => {
    const updatedPhotos = formData.photos.filter((_, i) => i !== index);
    setFormData({ ...formData, photos: updatedPhotos });
    setPhotoCount(updatedPhotos.length);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.photos.length !== 5) {
      alert("5 photos sont requises");
      return;
    }

    const data = new FormData();
    Object.keys(formData).forEach((key) => {
      if (key !== "photos") {
        data.append(key, formData[key]);
      }
    });

    formData.photos.forEach((photo, index) => {
      data.append(`photo${index + 1}`, photo);
    });

    try {
      await axios.post("http://localhost:8000/vehicules", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        withCredentials: true,
      });
      setShowSuccess(true);
      setTimeout(() => {
        navigate("/vehicules");
      }, 2000);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col items-center justify-center w-full gap-5 p-5 mt-5"
    >
      {showSuccess && (
        <div className="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg">
          Véhicule ajouté avec succès!
        </div>
      )}

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
          onChange={handlePhotoChange}
          required
        />
      </label>

      <div className="flex flex-col gap-2">
        <h1>Images téléchargées :</h1>
        <div className="flex gap-2">
          {formData.photos.map((image, index) => (
            <div key={index} className="relative">
              <img
                src={URL.createObjectURL(image)}
                alt={`Aperçu ${index}`}
                className="w-24 h-24 object-cover rounded-lg border"
              />
              <button
                type="button"
                onClick={() => handleRemovePhoto(index)}
                className="absolute top-0 right-0 bg-red-500 rounded-full p-1"
              >
                <XCircleIcon className="w-5 h-5 text-white" />
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="p-4 flex flex-col gap-4 w-full">
        <div className="flex gap-4 items-center">
          <select
            name="marque"
            value={formData.marque}
            onChange={(e) =>
              setFormData({ ...formData, marque: e.target.value })
            }
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
            onChange={(e) =>
              setFormData({ ...formData, modele: e.target.value })
            }
            className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
          />
        </div>

        <input
          type="number"
          name="prix"
          placeholder="Prix (€)"
          value={formData.prix}
          onChange={(e) => setFormData({ ...formData, prix: e.target.value })}
          className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
        />
        <input
          type="text"
          name="kilometrage"
          placeholder="Kilométrage (km)"
          value={formData.kilometrage}
          onChange={(e) =>
            setFormData({ ...formData, kilometrage: e.target.value })
          }
          className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
        />
        <input
          type="text"
          name="energie"
          placeholder="Type d'énergie"
          value={formData.energie}
          onChange={(e) =>
            setFormData({ ...formData, energie: e.target.value })
          }
          className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
        />
        <input
          type="text"
          name="type"
          placeholder="Type de véhicule"
          value={formData.type}
          onChange={(e) => setFormData({ ...formData, type: e.target.value })}
          className="p-3 rounded-lg focus:outline-indigo-600 shadow-md border border-gray-300"
        />
        <textarea
          name="description"
          placeholder="Description..."
          value={formData.description}
          onChange={(e) =>
            setFormData({ ...formData, description: e.target.value })
          }
          className="p-3 rounded-lg focus:outline-indigo-600 h-96 shadow-md border border-gray-300"
        ></textarea>
      </div>

      <button
        type="submit"
        className="bg-blue-500 text-white px-5 py-3 rounded-lg shadow-md hover:bg-blue-600 transition"
        disabled={photoCount !== 5}
      >
        Ajouter le véhicule
      </button>
    </form>
  );
}
