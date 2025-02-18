import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

export default function ListVehicules() {
  const [vehicules, setVehicules] = useState([]);
  const userId = localStorage.getItem("userId");
  console.log("userId:", userId);

  useEffect(() => {
    const fetchVehicules = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/vehicules`, {
          withCredentials: true,
        });
        console.log("response:", response.data);
        setVehicules(response.data);
      } catch (error) {
        console.error("Error fetching vehicles:", error);
      }
    };
    fetchVehicules();
  }, [userId]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Mes véhicules</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {vehicules.map((vehicule) => (
          <div
            key={vehicule.id}
            className="bg-white rounded-lg shadow-md overflow-hidden"
          >
            <img
              src={`http://localhost:8000/static/${vehicule.photo1}`}
              alt={`${vehicule.marque} ${vehicule.modele}`}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <h2 className="text-xl font-semibold">
                {vehicule.marque} {vehicule.modele}
              </h2>
              <p className="text-gray-600">{vehicule.prix} €</p>
              <p className="text-gray-500">{vehicule.kilometrage} km</p>
              <div className="mt-4">
                <Link
                  to={`/vehicules/${vehicule.id}`}
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Voir détails
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
