import api from './api';
export const startInterview=(accident_id,party_label)=>api.post('/api/interviews/start',{accident_id,party_label});
export const sendMessage=(id,message)=>api.post(`/api/interviews/${id}/message`,{message});
export const getInterview=(id)=>api.get(`/api/interviews/${id}`);
export const createStatement=(accident_id,party_label,raw_text)=>api.post('/api/statements',{accident_id,party_label,raw_text});
