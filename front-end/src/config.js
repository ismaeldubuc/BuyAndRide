const configs = {
  development: {
    API_URL: 'http://localhost:8000/api',
    STATIC_URL: 'http://localhost:8000/static'
  },
  production: {
    API_URL: 'http://35.180.232.202/api',
    STATIC_URL: 'http://35.180.232.202/static'
  }
};

const environment = import.meta.env.MODE === 'production' ? 'production' : 'development';
export const { API_URL, STATIC_URL } = configs[environment];

console.log("Configuration chargée:", { API_URL, STATIC_URL }); // Debug