import { useState, useEffect, createContext, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '@/lib/api';

// Create a context for authentication
const AuthContext = createContext(null);

// Provider component that wraps the app and makes auth available to any child component
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on mount
    const token = localStorage.getItem('token');
    if (token) {
      // Fetch user profile
      authApi.getProfile()
        .then(userData => {
          setUser(userData);
        })
        .catch(() => {
          // If token is invalid, remove it
          localStorage.removeItem('token');
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    try {
      const data = await authApi.login(email, password);
      localStorage.setItem('token', data.access_token);
      
      // Fetch user profile after login
      const userData = await authApi.getProfile();
      setUser(userData);
      
      return true;
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Hook for components to get the auth object and re-render when it changes
export const useAuth = () => {
  return useContext(AuthContext);
};

// Hook to protect routes that require authentication
export const useRequireAuth = (redirectUrl = '/login') => {
  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (auth.loading) return;
    if (!auth.isAuthenticated) {
      navigate(redirectUrl);
    }
  }, [auth, navigate, redirectUrl]);

  return auth;
};

