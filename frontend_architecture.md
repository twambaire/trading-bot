# Frontend Architecture

## Overview

The frontend of the trading bot is built with React, a popular JavaScript library for building user interfaces. The architecture follows a component-based approach with clear separation of concerns, making it modular, maintainable, and testable.

## Architecture Patterns

### 1. Component-Based Architecture

The frontend is built using a component-based architecture, where the UI is broken down into reusable components. Each component is responsible for a specific part of the UI and can be composed to build complex interfaces.

**Key Concepts:**
- **Components**: Reusable UI elements
- **Props**: Data passed to components
- **State**: Internal component data
- **Lifecycle Methods**: Methods called at different stages of a component's life

### 2. Context API for State Management

The Context API is used for global state management, allowing data to be shared across components without prop drilling.

**Key Concepts:**
- **Context**: A way to share data across the component tree
- **Provider**: A component that provides the context value
- **Consumer**: A component that consumes the context value
- **useContext**: A hook to access context values

### 3. Custom Hooks for Reusable Logic

Custom hooks are used to extract and reuse stateful logic across components.

**Key Concepts:**
- **Hooks**: Functions that let you use React features in functional components
- **Custom Hooks**: User-defined hooks that extract and reuse logic
- **Rules of Hooks**: Rules that must be followed when using hooks

### 4. API Client for Backend Communication

An API client is used to communicate with the backend API, abstracting away the details of HTTP requests.

**Key Concepts:**
- **API Client**: A module that handles API requests
- **Axios**: A popular HTTP client for making requests
- **Interceptors**: Functions that intercept requests and responses
- **Error Handling**: Handling API errors

## Component Hierarchy

The frontend is organized into a hierarchy of components, with each component responsible for a specific part of the UI.

```
App
├── Layout
│   ├── Header
│   ├── Sidebar
│   └── Footer
├── Pages
│   ├── Home
│   ├── Dashboard
│   ├── Strategies
│   ├── Backtester
│   └── Trading
└── Components
    ├── Common
    │   ├── Button
    │   ├── Input
    │   ├── Select
    │   └── Modal
    ├── Auth
    │   ├── LoginForm
    │   └── RegisterForm
    ├── Dashboard
    │   ├── PerformanceChart
    │   ├── StrategyCard
    │   └── TradeHistory
    ├── Strategies
    │   ├── StrategyList
    │   ├── StrategyForm
    │   └── StrategyEditor
    ├── Backtester
    │   ├── BacktestForm
    │   ├── BacktestResults
    │   └── BacktestChart
    └── Trading
        ├── TradingDashboard
        ├── OrderForm
        └── PositionList
```

## Component Interactions

The following diagram illustrates how the different components interact with each other:

```
+----------------+      +----------------+      +----------------+
|                |      |                |      |                |
|  Pages         |----->|  Components    |----->|  API Client    |
|  (Routes)      |      |  (UI Elements) |      |  (Backend      |
|                |<-----|                |<-----|  Communication) |
+----------------+      +----------------+      +----------------+
        |                      ^                       |
        |                      |                       |
        v                      |                       v
+----------------+      +----------------+      +----------------+
|                |      |                |      |                |
|  Contexts      |----->|  Hooks         |----->|  Utils         |
|  (State        |      |  (Reusable     |      |  (Helper       |
|  Management)   |<-----|  Logic)        |<-----|  Functions)    |
+----------------+      +----------------+      +----------------+
```

1. Pages define the routes and layout of the application.
2. Components render the UI elements and handle user interactions.
3. Contexts manage global state and provide it to components.
4. Hooks encapsulate reusable logic and provide it to components.
5. API Client communicates with the backend API.
6. Utils provide helper functions for common tasks.

## React Application Structure

### Main Application

The main application is defined in `App.jsx` and is responsible for setting up the React application, including routing, contexts, and global styles.

```jsx
// App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

import { AuthProvider } from './contexts/AuthContext';
import { theme } from './theme';
import Layout from './components/common/Layout';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Strategies from './pages/Strategies';
import Backtester from './pages/Backtester';
import Trading from './pages/Trading';
import Login from './pages/Login';
import Register from './pages/Register';
import PrivateRoute from './components/auth/PrivateRoute';

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/" element={<Layout />}>
              <Route index element={<Home />} />
              <Route path="dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
              <Route path="strategies" element={<PrivateRoute><Strategies /></PrivateRoute>} />
              <Route path="backtester" element={<PrivateRoute><Backtester /></PrivateRoute>} />
              <Route path="trading" element={<PrivateRoute><Trading /></PrivateRoute>} />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
```

### Pages

Pages are top-level components that represent different routes in the application. Each page is responsible for a specific feature or section of the application.

```jsx
// pages/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import { Container, Grid, Typography } from '@mui/material';

import { useAuth } from '../hooks/useAuth';
import { useApi } from '../hooks/useApi';
import PerformanceChart from '../components/dashboard/PerformanceChart';
import StrategyCard from '../components/dashboard/StrategyCard';
import TradeHistory from '../components/dashboard/TradeHistory';

const Dashboard = () => {
  const { user } = useAuth();
  const api = useApi();
  const [strategies, setStrategies] = useState([]);
  const [trades, setTrades] = useState([]);
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch strategies
        const strategiesResponse = await api.strategies.getStrategies();
        setStrategies(strategiesResponse.data);
        
        // Fetch trades
        const tradesResponse = await api.trading.getTrades();
        setTrades(tradesResponse.data);
        
        // Fetch performance
        const performanceResponse = await api.trading.getPerformance();
        setPerformance(performanceResponse.data);
        
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };
    
    fetchData();
  }, [api]);

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <PerformanceChart performance={performance} />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Typography variant="h5" component="h2" gutterBottom>
            Strategies
          </Typography>
          {strategies.map((strategy) => (
            <StrategyCard key={strategy.id} strategy={strategy} />
          ))}
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Typography variant="h5" component="h2" gutterBottom>
            Recent Trades
          </Typography>
          <TradeHistory trades={trades} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
```

### Components

Components are reusable UI elements that can be composed to build complex interfaces. Each component is responsible for a specific part of the UI.

```jsx
// components/dashboard/PerformanceChart.jsx
import React from 'react';
import { Card, CardContent, CardHeader } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PerformanceChart = ({ performance }) => {
  if (!performance || !performance.equity_curve) {
    return null;
  }

  // Transform data for the chart
  const data = performance.equity_curve.map((point) => ({
    date: new Date(point.date).toLocaleDateString(),
    equity: point.equity,
  }));

  return (
    <Card>
      <CardHeader title="Performance" />
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="equity" stroke="#8884d8" activeDot={{ r: 8 }} />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default PerformanceChart;
```

### Contexts

Contexts are used for global state management, allowing data to be shared across components without prop drilling.

```jsx
// contexts/AuthContext.jsx
import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      // Fetch user data
      axios.get('/api/v1/users/me')
        .then((response) => {
          setUser(response.data);
          setLoading(false);
        })
        .catch((error) => {
          localStorage.removeItem('token');
          delete axios.defaults.headers.common['Authorization'];
          setUser(null);
          setError(error.message);
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    try {
      const response = await axios.post('/api/v1/auth/login', { email, password });
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      setUser(user);
      setError(null);
      
      return user;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const register = async (email, password, name) => {
    try {
      const response = await axios.post('/api/v1/auth/register', { email, password, name });
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      setUser(user);
      setError(null);
      
      return user;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### Hooks

Hooks are used to extract and reuse stateful logic across components.

```jsx
// hooks/useAuth.js
import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

// hooks/useApi.js
import { useMemo } from 'react';
import axios from 'axios';

import { useAuth } from './useAuth';

export const useApi = () => {
  const { logout } = useAuth();
  
  return useMemo(() => {
    // Create API client
    const api = {
      auth: {
        login: (email, password) => axios.post('/api/v1/auth/login', { email, password }),
        register: (email, password, name) => axios.post('/api/v1/auth/register', { email, password, name }),
        logout: () => axios.post('/api/v1/auth/logout'),
      },
      users: {
        getMe: () => axios.get('/api/v1/users/me'),
        updateMe: (data) => axios.put('/api/v1/users/me', data),
      },
      strategies: {
        getStrategies: () => axios.get('/api/v1/strategies'),
        getStrategy: (id) => axios.get(`/api/v1/strategies/${id}`),
        createStrategy: (data) => axios.post('/api/v1/strategies', data),
        updateStrategy: (id, data) => axios.put(`/api/v1/strategies/${id}`, data),
        deleteStrategy: (id) => axios.delete(`/api/v1/strategies/${id}`),
      },
      backtests: {
        getBacktests: () => axios.get('/api/v1/backtests'),
        getBacktest: (id) => axios.get(`/api/v1/backtests/${id}`),
        createBacktest: (data) => axios.post('/api/v1/backtests', data),
        deleteBacktest: (id) => axios.delete(`/api/v1/backtests/${id}`),
        getBacktestResults: (id) => axios.get(`/api/v1/backtests/${id}/results`),
        getBacktestChart: (id) => axios.get(`/api/v1/backtests/${id}/chart`),
      },
      trading: {
        getAccounts: () => axios.get('/api/v1/trading/accounts'),
        getAccount: (id) => axios.get(`/api/v1/trading/accounts/${id}`),
        createAccount: (data) => axios.post('/api/v1/trading/accounts', data),
        deleteAccount: (id) => axios.delete(`/api/v1/trading/accounts/${id}`),
        getOrders: () => axios.get('/api/v1/trading/orders'),
        getOrder: (id) => axios.get(`/api/v1/trading/orders/${id}`),
        createOrder: (data) => axios.post('/api/v1/trading/orders', data),
        cancelOrder: (id) => axios.delete(`/api/v1/trading/orders/${id}`),
        getPositions: () => axios.get('/api/v1/trading/positions'),
        getPosition: (id) => axios.get(`/api/v1/trading/positions/${id}`),
        closePosition: (id) => axios.delete(`/api/v1/trading/positions/${id}`),
        getPerformance: () => axios.get('/api/v1/trading/performance'),
        getTrades: () => axios.get('/api/v1/trading/trades'),
      },
    };
    
    // Add response interceptor for handling 401 errors
    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          logout();
        }
        return Promise.reject(error);
      }
    );
    
    return api;
  }, [logout]);
};
```

## Backtester Interface

The backtester interface is a key component of the frontend that allows users to backtest trading strategies on historical data.

### Backtester Form

The backtester form allows users to configure and run backtests.

```jsx
// components/backtester/BacktestForm.jsx
import React, { useState } from 'react';
import { Button, Card, CardContent, CardHeader, FormControl, Grid, InputLabel, MenuItem, Select, TextField } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';

import { useApi } from '../../hooks/useApi';

const BacktestForm = ({ strategies, onBacktestCreated }) => {
  const api = useApi();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    strategy_id: '',
    start_date: new Date(new Date().setFullYear(new Date().getFullYear() - 1)),
    end_date: new Date(),
    parameters: {},
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleDateChange = (name, value) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleStrategyChange = (e) => {
    const strategyId = e.target.value;
    const strategy = strategies.find((s) => s.id === strategyId);
    
    setFormData((prev) => ({
      ...prev,
      strategy_id: strategyId,
      parameters: strategy ? { ...strategy.parameters } : {},
    }));
  };

  const handleParameterChange = (name, value) => {
    setFormData((prev) => ({
      ...prev,
      parameters: {
        ...prev.parameters,
        [name]: value,
      },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.backtests.createBacktest(formData);
      
      setLoading(false);
      onBacktestCreated(response.data);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  const selectedStrategy = strategies.find((s) => s.id === formData.strategy_id);

  return (
    <Card>
      <CardHeader title="Create Backtest" />
      <CardContent>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                multiline
                rows={2}
              />
            </Grid>
            
            <Grid item xs={12}>
              <FormControl fullWidth required>
                <InputLabel>Strategy</InputLabel>
                <Select
                  name="strategy_id"
                  value={formData.strategy_id}
                  onChange={handleStrategyChange}
                >
                  {strategies.map((strategy) => (
                    <MenuItem key={strategy.id} value={strategy.id}>
                      {strategy.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DatePicker
                  label="Start Date"
                  value={formData.start_date}
                  onChange={(value) => handleDateChange('start_date', value)}
                  renderInput={(params) => <TextField {...params} fullWidth required />}
                />
              </LocalizationProvider>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DatePicker
                  label="End Date"
                  value={formData.end_date}
                  onChange={(value) => handleDateChange('end_date', value)}
                  renderInput={(params) => <TextField {...params} fullWidth required />}
                />
              </LocalizationProvider>
            </Grid>
            
            {selectedStrategy && Object.entries(formData.parameters).map(([name, value]) => (
              <Grid item xs={12} md={6} key={name}>
                <TextField
                  fullWidth
                  label={name}
                  value={value}
                  onChange={(e) => handleParameterChange(name, e.target.value)}
                  type={typeof value === 'number' ? 'number' : 'text'}
                />
              </Grid>
            ))}
            
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={loading}
              >
                {loading ? 'Running...' : 'Run Backtest'}
              </Button>
              
              {error && (
                <Typography color="error" sx={{ mt: 2 }}>
                  {error}
                </Typography>
              )}
            </Grid>
          </Grid>
        </form>
      </CardContent>
    </Card>
  );
};

export default BacktestForm;
```

### Backtest Results

The backtest results component displays the results of a backtest.

```jsx
// components/backtester/BacktestResults.jsx
import React from 'react';
import { Card, CardContent, CardHeader, Grid, Typography } from '@mui/material';

import BacktestChart from './BacktestChart';
import BacktestMetrics from './BacktestMetrics';
import BacktestTrades from './BacktestTrades';

const BacktestResults = ({ backtest }) => {
  if (!backtest || !backtest.results) {
    return null;
  }

  return (
    <Card>
      <CardHeader title={`Backtest Results: ${backtest.name}`} />
      <CardContent>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <BacktestChart data={backtest.results.equity_curve} />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <BacktestMetrics metrics={backtest.results.metrics} />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <BacktestTrades trades={backtest.results.trades} />
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default BacktestResults;
```

## Trading Interface

The trading interface allows users to manage trading accounts, place orders, and monitor positions.

### Trading Dashboard

The trading dashboard provides an overview of the user's trading activity.

```jsx
// components/trading/TradingDashboard.jsx
import React from 'react';
import { Card, CardContent, CardHeader, Grid, Typography } from '@mui/material';

import AccountSummary from './AccountSummary';
import PositionList from './PositionList';
import OrderList from './OrderList';

const TradingDashboard = ({ account, positions, orders }) => {
  if (!account) {
    return (
      <Typography variant="body1">
        No trading account connected. Please connect an account to start trading.
      </Typography>
    );
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <AccountSummary account={account} />
      </Grid>
      
      <Grid item xs={12} md={6}>
        <Card>
          <CardHeader title="Positions" />
          <CardContent>
            <PositionList positions={positions} />
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} md={6}>
        <Card>
          <CardHeader title="Orders" />
          <CardContent>
            <OrderList orders={orders} />
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default TradingDashboard;
```

### Order Form

The order form allows users to place new orders.

```jsx
// components/trading/OrderForm.jsx
import React, { useState } from 'react';
import { Button, Card, CardContent, CardHeader, FormControl, Grid, InputLabel, MenuItem, Select, TextField, Typography } from '@mui/material';

import { useApi } from '../../hooks/useApi';

const OrderForm = ({ account, onOrderCreated }) => {
  const api = useApi();
  const [formData, setFormData] = useState({
    symbol: '',
    order_type: 'market',
    side: 'buy',
    quantity: 1,
    price: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.trading.createOrder({
        ...formData,
        trading_account_id: account.id,
      });
      
      setLoading(false);
      setFormData({
        symbol: '',
        order_type: 'market',
        side: 'buy',
        quantity: 1,
        price: null,
      });
      
      onOrderCreated(response.data);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader title="Place Order" />
      <CardContent>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Symbol"
                name="symbol"
                value={formData.symbol}
                onChange={handleChange}
                required
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Order Type</InputLabel>
                <Select
                  name="order_type"
                  value={formData.order_type}
                  onChange={handleChange}
                >
                  <MenuItem value="market">Market</MenuItem>
                  <MenuItem value="limit">Limit</MenuItem>
                  <MenuItem value="stop">Stop</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Side</InputLabel>
                <Select
                  name="side"
                  value={formData.side}
                  onChange={handleChange}
                >
                  <MenuItem value="buy">Buy</MenuItem>
                  <MenuItem value="sell">Sell</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Quantity"
                name="quantity"
                type="number"
                value={formData.quantity}
                onChange={handleChange}
                required
              />
            </Grid>
            
            {formData.order_type !== 'market' && (
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Price"
                  name="price"
                  type="number"
                  value={formData.price}
                  onChange={handleChange}
                  required
                />
              </Grid>
            )}
            
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={loading}
              >
                {loading ? 'Placing Order...' : 'Place Order'}
              </Button>
              
              {error && (
                <Typography color="error" sx={{ mt: 2 }}>
                  {error}
                </Typography>
              )}
            </Grid>
          </Grid>
        </form>
      </CardContent>
    </Card>
  );
};

export default OrderForm;
```

## Authentication

The authentication components handle user login and registration.

### Login Form

The login form allows users to authenticate with the application.

```jsx
// components/auth/LoginForm.jsx
import React, { useState } from 'react';
import { Button, Card, CardContent, CardHeader, TextField, Typography } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';

import { useAuth } from '../../hooks/useAuth';

const LoginForm = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);
      
      await login(formData.email, formData.password);
      
      setLoading(false);
      navigate('/dashboard');
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader title="Login" />
      <CardContent>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            required
            margin="normal"
          />
          
          <TextField
            fullWidth
            label="Password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            required
            margin="normal"
          />
          
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
            fullWidth
            sx={{ mt: 2 }}
          >
            {loading ? 'Logging in...' : 'Login'}
          </Button>
          
          {error && (
            <Typography color="error" sx={{ mt: 2 }}>
              {error}
            </Typography>
          )}
          
          <Typography sx={{ mt: 2 }}>
            Don't have an account?{' '}
            <RouterLink to="/register">Register</RouterLink>
          </Typography>
        </form>
      </CardContent>
    </Card>
  );
};

export default LoginForm;
```

## Responsive Design

The frontend is designed to be responsive, adapting to different screen sizes and devices.

```jsx
// components/common/Layout.jsx
import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Box, CssBaseline, Drawer, useMediaQuery, useTheme } from '@mui/material';

import Header from './Header';
import Sidebar from './Sidebar';
import Footer from './Footer';

const Layout = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawerWidth = 240;

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      
      <Header
        drawerWidth={drawerWidth}
        onDrawerToggle={handleDrawerToggle}
      />
      
      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          <Sidebar />
        </Drawer>
        
        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          <Sidebar />
        </Drawer>
      </Box>
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
          {/* Toolbar placeholder to push content below app bar */}
          <Box sx={{ ...theme.mixins.toolbar }} />
          
          {/* Main content */}
          <Box sx={{ flexGrow: 1 }}>
            <Outlet />
          </Box>
          
          {/* Footer */}
          <Footer />
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;
```

## API Client

The API client handles communication with the backend API, abstracting away the details of HTTP requests.

```jsx
// api/client.js
import axios from 'axios';

// Create axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 errors
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

## WebSocket Integration

The frontend uses WebSockets for real-time updates from the backend.

```jsx
// hooks/useWebSocket.js
import { useEffect, useRef, useState } from 'react';

import { useAuth } from './useAuth';

export const useWebSocket = (url) => {
  const { user } = useAuth();
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState([]);
  const socketRef = useRef(null);

  useEffect(() => {
    if (!user) {
      return;
    }

    // Create WebSocket connection
    const token = localStorage.getItem('token');
    const socket = new WebSocket(`${url}?token=${token}`);
    socketRef.current = socket;

    // Connection opened
    socket.addEventListener('open', () => {
      setIsConnected(true);
    });

    // Listen for messages
    socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      setMessages((prev) => [...prev, message]);
    });

    // Connection closed
    socket.addEventListener('close', () => {
      setIsConnected(false);
    });

    // Clean up on unmount
    return () => {
      socket.close();
    };
  }, [url, user]);

  // Send message
  const sendMessage = (message) => {
    if (socketRef.current && isConnected) {
      socketRef.current.send(JSON.stringify(message));
    }
  };

  // Clear messages
  const clearMessages = () => {
    setMessages([]);
  };

  return {
    isConnected,
    messages,
    sendMessage,
    clearMessages,
  };
};
```

## Conclusion

The frontend architecture is designed to be modular, maintainable, and testable. It follows a component-based approach with clear separation of concerns, making it easy to extend and modify as requirements evolve. The React library provides a solid foundation for building interactive UIs, while the Context API and custom hooks provide robust state management and reusable logic.

