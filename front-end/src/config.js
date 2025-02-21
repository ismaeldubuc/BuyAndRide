const configs = {
  development: {
    API_URL: 'http://localhost:8000/api',
    STATIC_URL: 'http://localhost:8000/static'
  },
  production: {
    API_URL: 'https://main.d3bzhfj3yrtaed.amplifyapp.com/api',
    STATIC_URL: 'https://votre-bucket-s3.s3.amazonaws.com'
  }
};

const environment = process.env.NODE_ENV || 'development';
export const { API_URL, STATIC_URL } = configs[environment];