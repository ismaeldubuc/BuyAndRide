import React from 'react'

function Accueil() {
  return (
    <div className="accueil-container" style={{ 
      display: 'flex', 
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      background: '#f5f5f5'
    }}>
      <h1 style={{ 
        fontSize: '2.5rem', 
        marginBottom: '2rem',
        color: '#333'
      }}>
        Bienvenue sur Buy And Ride
      </h1>
      <div style={{
        display: 'flex',
        gap: '1rem'
      }}>
        <button 
          style={{
            padding: '0.8rem 2rem',
            fontSize: '1.1rem',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            transition: 'background-color 0.3s'
          }}
          onClick={() => window.location.href = '/login-page'}
        >
          Se connecter
        </button>
        <button 
          style={{
            padding: '0.8rem 2rem',
            fontSize: '1.1rem',
            backgroundColor: '#2196F3',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            transition: 'background-color 0.3s'
          }}
          onClick={() => window.location.href = '/register-page'}
        >
          S'inscrire
        </button>
      </div>
    </div>
  )
}

export default Accueil
