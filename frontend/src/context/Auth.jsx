import { createContext, useContext, useState, useEffect, use } from "react";
import api from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({children}){
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(()=>{
        const token = localStorage.getItem('access_token');
        if (token){
            api.get('/api/auth/me/')
            .then((res) => setUser(res.data))
            .catch(()=>{
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
            })
            .finally(()=>setLoading(false));
        }else {
            setLoading(false);
        }
    }, []);

    const login = async (username, password) => {
        const res = await api.post('/api/auth/login/', 
            {username, password});
        localStorage.setItem('access_token', res.data.access);
        localStorage.setItem('refresh_token', res.data.refresh);
        const me = await api.get('/api/auth/me/');
        setUser(me.data);
        return me.data;
    };

    const register = async (username, email, password) => {
        await api.post('/api/auth/register/', 
            {username, email, password});
        return login(username, password);
    };
    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        api.post('/api/auth/logout/').catch(()=>{});
    };

    return (
        <AuthContext.Provider value={{user, loading, login, register, logout}}>
            {children}
        </AuthContext.Provider>
    );
}
export const useAuth = () => useContext(AuthContext);