const configs = {
  development: {
    API_URL: 'http://localhost:8000/api',
    STATIC_URL: 'http://localhost:8000/static'
  },
  production: {
    API_URL: 'https://amplify.d3bzhfj3yrtaed.amplifyapp.com/api',
    STATIC_URL: 'https://amplify.d3bzhfj3yrtaed.amplifyapp.com/static'
  }
};

const environment = import.meta.env.PROD ? 'production' : 'development';
export const { API_URL, STATIC_URL } = configs[environment];