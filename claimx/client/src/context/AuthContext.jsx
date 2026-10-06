import {createContext,useContext,useEffect,useState} from 'react';
import {me,login as doLogin,register as doRegister,logout as doLogout} from '../services/authService';
const C=createContext(null);
export function AuthProvider({children}){const [user,setUser]=useState(null);const [loading,setLoading]=useState(true);useEffect(()=>{if(localStorage.getItem('claimx_token'))me().then(setUser).catch(()=>doLogout()).finally(()=>setLoading(false));else setLoading(false)},[]);const login=async d=>{await doLogin(d);setUser(await me())};const register=async d=>{await doRegister(d);setUser(await me())};const logout=()=>{doLogout();setUser(null)};return <C.Provider value={{user,loading,login,register,logout}}>{children}</C.Provider>}
export const useAuth=()=>useContext(C);
