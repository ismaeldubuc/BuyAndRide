import { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export default function AddVehicule() {
  const navigate = useNavigate()
  const [showSuccess, setShowSuccess] = useState(false)
  const [photoCount, setPhotoCount] = useState(0)
  const [formData, setFormData] = useState({
    marque: '',
    modele: '',
    prix: '',
    kilometrage: '',
    energie: '',
    type: '',
    description: '',
    photos: []
  })

  const handlePhotoChange = (e) => {
    const files = Array.from(e.target.files)
    if (files.length !== 5) {
      alert("Veuillez sélectionner exactement 5 photos")
      e.target.value = ''
      setPhotoCount(0)
      setFormData({...formData, photos: []})
      return
    }
    setPhotoCount(files.length)
    setFormData({...formData, photos: files})
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (formData.photos.length !== 5) {
      alert("5 photos sont requises")
      return
    }

    const data = new FormData()
    Object.keys(formData).forEach(key => {
      if (key !== 'photos') {
        data.append(key, formData[key])
      }
    })
    
    formData.photos.forEach((photo, index) => {
      data.append(`photo${index + 1}`, photo)
    })

    try {
      await axios.post('http://localhost:8000/vehicules', data, {
        withCredentials: true
      })
      setShowSuccess(true)
      setTimeout(() => {
        navigate('/vehicules')
      }, 2000)
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="container mx-auto p-4">
      {showSuccess && (
        <div className="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg">
          Véhicule ajouté avec succès!
        </div>
      )}

      <h1 className="text-3xl font-bold mb-6">Ajouter un véhicule</h1>
      <form onSubmit={handleSubmit} className="max-w-lg mx-auto bg-white p-6 rounded-lg shadow-md">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-2">Marque</label>
            <input
              type="text"
              className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={formData.marque}
              onChange={e => setFormData({...formData, marque: e.target.value})}
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-2">Modèle</label>
            <input
              type="text"
              className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={formData.modele}
              onChange={e => setFormData({...formData, modele: e.target.value})}
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-2">Prix (€)</label>
            <input
              type="number"
              className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={formData.prix}
              onChange={e => setFormData({...formData, prix: e.target.value})}
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-2">Kilométrage</label>
            <input
              type="number"
              className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={formData.kilometrage}
              onChange={e => setFormData({...formData, kilometrage: e.target.value})}
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-2">Énergie</label>
            <input
              type="text"
              className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={formData.energie}
              onChange={e => setFormData({...formData, energie: e.target.value})}
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-2">Type</label>
            <input
              type="text"
              className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={formData.type}
              onChange={e => setFormData({...formData, type: e.target.value})}
              required
            />
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-2">Description</label>
          <textarea
            className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.description}
            onChange={e => setFormData({...formData, description: e.target.value})}
            rows="4"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-700 font-semibold mb-2">
            Photos (5 photos requises)
          </label>
          <input
            type="file"
            multiple
            accept="image/*"
            onChange={handlePhotoChange}
            className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            {photoCount === 5 ?
              "✅ 5 photos sélectionnées" :
              "❌ Veuillez sélectionner exactement 5 photos"}
          </p>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-600 transition duration-300"
          disabled={photoCount !== 5}
        >
          Ajouter le véhicule
        </button>
      </form>
    </div>
  )
}