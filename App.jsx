import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from '@/hooks/useAuth';
import MainLayout from '@/components/layout/MainLayout';
import ProtectedRoute from '@/components/ProtectedRoute';
import Dashboard from '@/pages/Dashboard';
import Strategies from '@/pages/Strategies';
import Backtests from '@/pages/Backtests';
import Trading from '@/pages/Trading';
import Settings from '@/pages/Settings';
import Login from '@/pages/Login';
import NotFound from '@/pages/NotFound';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          
          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route element={<MainLayout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/strategies" element={<Strategies />} />
              <Route path="/backtests" element={<Backtests />} />
              <Route path="/trading" element={<Trading />} />
              <Route path="/settings" element={<Settings />} />
            </Route>
          </Route>
          
          {/* 404 route */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
