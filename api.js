/**
 * API client for communicating with the backend
 */

// Base URL for API requests
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Make an API request with authentication
 * 
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Request options
 * @returns {Promise<any>} - Response data
 */
async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const config = {
    ...options,
    headers,
  };
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
  
  // Handle 401 Unauthorized (token expired or invalid)
  if (response.status === 401) {
    localStorage.removeItem('token');
    window.location.href = '/login';
    throw new Error('Session expired. Please log in again.');
  }
  
  // Handle other errors
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'An error occurred');
  }
  
  // Return JSON response or empty object if no content
  return response.status === 204 ? {} : await response.json();
}

/**
 * Authentication API
 */
export const authApi = {
  /**
   * Login with email and password
   * 
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise<Object>} - Auth token and user data
   */
  login: async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error('Invalid email or password');
    }
    
    return response.json();
  },
  
  /**
   * Get current user profile
   * 
   * @returns {Promise<Object>} - User profile data
   */
  getProfile: () => apiRequest('/api/users/me'),
};

/**
 * Strategies API
 */
export const strategiesApi = {
  /**
   * Get all strategies
   * 
   * @returns {Promise<Array>} - List of strategies
   */
  getAll: () => apiRequest('/api/strategies'),
  
  /**
   * Get strategy by ID
   * 
   * @param {number} id - Strategy ID
   * @returns {Promise<Object>} - Strategy data
   */
  getById: (id) => apiRequest(`/api/strategies/${id}`),
  
  /**
   * Create a new strategy
   * 
   * @param {Object} data - Strategy data
   * @returns {Promise<Object>} - Created strategy
   */
  create: (data) => apiRequest('/api/strategies', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  /**
   * Update a strategy
   * 
   * @param {number} id - Strategy ID
   * @param {Object} data - Strategy data
   * @returns {Promise<Object>} - Updated strategy
   */
  update: (id, data) => apiRequest(`/api/strategies/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  
  /**
   * Delete a strategy
   * 
   * @param {number} id - Strategy ID
   * @returns {Promise<Object>} - Deleted strategy
   */
  delete: (id) => apiRequest(`/api/strategies/${id}`, {
    method: 'DELETE',
  }),
};

/**
 * Backtests API
 */
export const backtestsApi = {
  /**
   * Get all backtests
   * 
   * @returns {Promise<Array>} - List of backtests
   */
  getAll: () => apiRequest('/api/backtests'),
  
  /**
   * Get backtest by ID
   * 
   * @param {number} id - Backtest ID
   * @returns {Promise<Object>} - Backtest data
   */
  getById: (id) => apiRequest(`/api/backtests/${id}`),
  
  /**
   * Create a new backtest
   * 
   * @param {Object} data - Backtest data
   * @returns {Promise<Object>} - Created backtest
   */
  create: (data) => apiRequest('/api/backtests', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  /**
   * Run a backtest
   * 
   * @param {number} id - Backtest ID
   * @returns {Promise<Object>} - Backtest results
   */
  run: (id) => apiRequest(`/api/backtests/${id}/run`, {
    method: 'POST',
  }),
  
  /**
   * Get backtest results
   * 
   * @param {number} id - Backtest ID
   * @returns {Promise<Object>} - Backtest results
   */
  getResults: (id) => apiRequest(`/api/backtests/${id}/results`),
  
  /**
   * Get backtest report URL
   * 
   * @param {number} id - Backtest ID
   * @returns {string} - Backtest report URL
   */
  getReportUrl: (id) => `${API_BASE_URL}/api/backtests/${id}/report`,
  
  /**
   * Delete a backtest
   * 
   * @param {number} id - Backtest ID
   * @returns {Promise<Object>} - Deleted backtest
   */
  delete: (id) => apiRequest(`/api/backtests/${id}`, {
    method: 'DELETE',
  }),
};

/**
 * Trading API
 */
export const tradingApi = {
  /**
   * Get all trading accounts
   * 
   * @returns {Promise<Array>} - List of trading accounts
   */
  getAccounts: () => apiRequest('/api/trading/accounts'),
  
  /**
   * Get account by ID
   * 
   * @param {number} id - Account ID
   * @returns {Promise<Object>} - Account data
   */
  getAccountById: (id) => apiRequest(`/api/trading/accounts/${id}`),
  
  /**
   * Get all positions
   * 
   * @param {number} accountId - Account ID
   * @returns {Promise<Array>} - List of positions
   */
  getPositions: (accountId) => apiRequest(`/api/trading/accounts/${accountId}/positions`),
  
  /**
   * Get all orders
   * 
   * @param {number} accountId - Account ID
   * @returns {Promise<Array>} - List of orders
   */
  getOrders: (accountId) => apiRequest(`/api/trading/accounts/${accountId}/orders`),
  
  /**
   * Create a new order
   * 
   * @param {number} accountId - Account ID
   * @param {Object} data - Order data
   * @returns {Promise<Object>} - Created order
   */
  createOrder: (accountId, data) => apiRequest(`/api/trading/accounts/${accountId}/orders`, {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  /**
   * Cancel an order
   * 
   * @param {number} accountId - Account ID
   * @param {number} orderId - Order ID
   * @returns {Promise<Object>} - Cancelled order
   */
  cancelOrder: (accountId, orderId) => apiRequest(`/api/trading/accounts/${accountId}/orders/${orderId}`, {
    method: 'DELETE',
  }),
  
  /**
   * Close a position
   * 
   * @param {number} accountId - Account ID
   * @param {number} positionId - Position ID
   * @returns {Promise<Object>} - Closed position
   */
  closePosition: (accountId, positionId) => apiRequest(`/api/trading/accounts/${accountId}/positions/${positionId}/close`, {
    method: 'POST',
  }),
};

