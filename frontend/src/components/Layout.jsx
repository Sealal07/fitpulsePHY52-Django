import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="layout">
      <header className="header">
        <Link to="/templates" className="logo">FitPulse Lite</Link>
        {user && (
          <nav className="nav">
            <Link to="/templates">Программы</Link>
            <Link to="/sessions">Тренировки</Link>
            <Link to="/prs">Рекорды</Link>
            <span className="user">{user.username}</span>
            <button onClick={handleLogout} className="small">Выйти</button>
          </nav>
        )}
      </header>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}