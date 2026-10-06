import api from './api';
export const login=async(data)=>{const r=await api.post('/api/auth/login',data);localStorage.setItem('claimx_token',r.data.access_token);return r.data};
export const register=async(data)=>{const r=await api.post('/api/auth/register',data);localStorage.setItem('claimx_token',r.data.access_token);return r.data};
export const me=async()=> (await api.get('/api/auth/me')).data;
export const logout=()=>localStorage.removeItem('claimx_token');
