import axios from "axios";

const api = axios.create({
    // пустая строка из-за прокси
    baseURL: '/',
    headers: {
        'Content-Type': 'application/json'
    },
});
// подставляем токен если он есть
api.interceptors.request.use((config)=>{
    const token = localStorage.getItem('access_token');
    if (token){
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
})
// если 401 - чистим токен и редирект на логин
api.interceptors.response.use((response)=>response, (error)=>{
    if (error.response && error.response.status === 401){
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        if (window.location.pathname !== '/login'){
            window.location.href = '/login';
        }
    }
    return Promise.reject(error);
})

export default api;