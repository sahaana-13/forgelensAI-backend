import {Bell,ShieldCheck} from 'lucide-react';
import {useAuth} from '../context/AuthContext';
export default function Navbar({title,subtitle}){const {user}=useAuth();return <header className="navbar"><div><h1>{title}</h1>{subtitle&&<p>{subtitle}</p>}</div><div className="nav-right"><span className="security"><ShieldCheck size={15}/> Secure workspace</span><Bell size={19}/><div className="avatar">{user?.email?.[0]?.toUpperCase()}</div></div></header>}
