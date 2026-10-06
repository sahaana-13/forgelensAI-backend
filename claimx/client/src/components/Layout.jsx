import Sidebar from './Sidebar';
export default function Layout({children}){return <div className="app-shell"><Sidebar/><main className="main"><div className="content">{children}</div></main></div>}
