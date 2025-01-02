// import axios from 'axios'

// const api = axios.create({
//     baseURL: 'http://localhost:8000',
// });

// export default api;

import axios from 'axios';

const api = axios.create({
    baseURL: process.env.NODE_ENV === 'production' 
        ? 'http://aws-finance-app-env.eba-ijbmy6jm.us-east-1.elasticbeanstalk.com'  // Production URL
        : 'http://localhost:8000',  // Local development URL
});

export default api;
