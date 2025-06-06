import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { 
  LayoutDashboard, 
  LineChart, 
  Settings, 
  TrendingUp, 
  BookOpen,
  LogOut
} from 'lucide-react';
import { cn } from '@/lib/utils';

const Sidebar = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  
  const navItems = [
    { to: '/', label: 'Dashboard', icon: <LayoutDashboard className="h-5 w-5" /> },
    { to: '/strategies', label: 'Strategies', icon: <BookOpen className="h-5 w-5" /> },
    { to: '/backtests', label: 'Backtests', icon: <LineChart className="h-5 w-5" /> },
    { to: '/trading', label: 'Trading', icon: <TrendingUp className="h-5 w-5" /> },
    { to: '/settings', label: 'Settings', icon: <Settings className="h-5 w-5" /> },
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside className="w-64 bg-sidebar text-sidebar-foreground border-r border-sidebar-border flex flex-col">
      <div className="p-4 border-b border-sidebar-border">
        <h1 className="text-xl font-bold">Trading Bot</h1>
      </div>
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) => cn(
                  "flex items-center gap-3 px-3 py-2 rounded-md transition-colors",
                  isActive 
                    ? "bg-sidebar-primary text-sidebar-primary-foreground" 
                    : "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
                )}
                end={item.to === '/'}
              >
                {item.icon}
                <span>{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
      <div className="p-4 border-t border-sidebar-border">
        <button 
          className="flex items-center gap-3 px-3 py-2 w-full rounded-md hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors"
          onClick={handleLogout}
        >
          <LogOut className="h-5 w-5" />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;

