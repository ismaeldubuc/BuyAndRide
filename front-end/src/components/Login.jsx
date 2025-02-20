import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import logo from "../assets/logo.svg"
function Login() {

  const [showPassword, setShowPassword] = useState(false);


  const [formData, setFormData] = React.useState({
    email: '',
    password: ''
  });

  const [error, setError] = React.useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('https://main.d3bzhfj3yrtaed.amplifyapp.com/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            email: formData.email,
            password: formData.password
        }),        
        credentials: 'include'
    });    

      const data = await response.json();

      if (response.ok) {
        navigate('/profile-page');
      } else {
        setError(data.message || 'Identifiants incorrects');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Une erreur est survenue, veuillez réessayer.');
    }
  };

  return (
    <div>
      <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <img
            alt="Logo Buy and Ride" 
            src={logo}
            className="mx-auto h-55 w-auto"
          />
          <h2 className="mt-10 text-center text-2xl font-bold tracking-tight text-gray-900">
            Sign in to your account
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-100 border border-red-400 rounded-md">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-900">
                Email address
              </label>
              <div className="mt-2">
                <input
                  id="email"
                  name="email"
                  type="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  autoComplete="email"
                  className="block w-full border border-gray-300 rounded-md bg-gray-50 px-3 py-1.5 text-base text-gray-900 outline-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-indigo-600 sm:text-sm"
                />
              </div>
            </div>

           

<div>
  <div className="flex items-center justify-between">
    <label htmlFor="password" className="block text-sm font-medium text-gray-900">
      Password
    </label>
  </div>
  <div className="mt-2 relative">
    <input
      id="password"
      name="password"
      type={showPassword ? "text" : "password"}
      required
      value={formData.password}
      onChange={handleChange}
      autoComplete="current-password"
      className="block w-full border border-gray-300 rounded-md bg-gray-50 px-3 py-1.5 text-base text-gray-900 outline-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-indigo-600 sm:text-sm"
    />
    <button
      type="button"
      className="absolute inset-y-0 right-0 flex items-center pr-3"
      onClick={() => setShowPassword(!showPassword)}
    >
      {showPassword ? (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-500">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
        </svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-500">
          <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      )}
    </button>
  </div>
</div>


            <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-[#31B057] px-3 py-1.5 text-sm font-semibold text-white shadow-xs hover:bg-[#2a9b4d] focus-visible:outline-2 focus-visible:outline-[#31B057]"
              >
                Sign in
              </button>
            </div>
          </form>

          <p className="mt-10 text-center text-sm text-gray-500">
            Not a member yet?{' '}
            <a href="/register-page" className="font-semibold text-primary-600 hover:text-[#2a9b4d] hover:underline ">
              Sign up
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
