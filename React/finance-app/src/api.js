// import axios from 'axios'

// const api = axios.create({
//     baseURL: 'http://localhost:8000',
// });

// export default api;

import axios from 'axios';

const api = axios.create({
    baseURL: process.env.NODE_ENV === 'production' 
        ? '/api'  // Production URL
        : 'http://localhost:8000',  // Local development URL
});

export default api;
