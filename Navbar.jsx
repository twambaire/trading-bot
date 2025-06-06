import { Bell, User } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { ThemeToggle } from '@/components/ThemeToggle';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="border-b border-border bg-background">
      <div className="flex h-16 items-center justify-between px-6">
        <div className="flex items-center gap-4">
          <h2 className="text-lg font-semibold">Dashboard</h2>
        </div>
        <div className="flex items-center gap-4">
          <ThemeToggle />
          <Button variant="ghost" size="icon">
            <Bell className="h-5 w-5" />
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="rounded-full">
                <User className="h-5 w-5" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>
                {user?.email || 'My Account'}
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => navigate('/settings')}>
                Profile
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => navigate('/settings')}>
                Settings
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={handleLogout}>
                Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
};

export default Navbar;

