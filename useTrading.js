import { useState, useEffect } from 'react';
import { tradingApi } from '@/lib/api';

export function useTrading() {
  const [accounts, setAccounts] = useState([]);
  const [positions, setPositions] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState({
    accounts: true,
    positions: false,
    orders: false,
  });
  const [error, setError] = useState({
    accounts: null,
    positions: null,
    orders: null,
  });

  const fetchAccounts = async () => {
    setLoading((prev) => ({ ...prev, accounts: true }));
    setError((prev) => ({ ...prev, accounts: null }));
    try {
      const data = await tradingApi.getAccounts();
      setAccounts(data);
      
      // If we have accounts, fetch positions and orders for the first account
      if (data.length > 0) {
        fetchPositions(data[0].id);
        fetchOrders(data[0].id);
      }
    } catch (err) {
      setError((prev) => ({ ...prev, accounts: err.message || 'Failed to fetch accounts' }));
    } finally {
      setLoading((prev) => ({ ...prev, accounts: false }));
    }
  };

  const fetchPositions = async (accountId) => {
    if (!accountId) return;
    
    setLoading((prev) => ({ ...prev, positions: true }));
    setError((prev) => ({ ...prev, positions: null }));
    try {
      const data = await tradingApi.getPositions(accountId);
      setPositions(data);
    } catch (err) {
      setError((prev) => ({ ...prev, positions: err.message || 'Failed to fetch positions' }));
    } finally {
      setLoading((prev) => ({ ...prev, positions: false }));
    }
  };

  const fetchOrders = async (accountId) => {
    if (!accountId) return;
    
    setLoading((prev) => ({ ...prev, orders: true }));
    setError((prev) => ({ ...prev, orders: null }));
    try {
      const data = await tradingApi.getOrders(accountId);
      setOrders(data);
    } catch (err) {
      setError((prev) => ({ ...prev, orders: err.message || 'Failed to fetch orders' }));
    } finally {
      setLoading((prev) => ({ ...prev, orders: false }));
    }
  };

  useEffect(() => {
    fetchAccounts();
  }, []);

  const createOrder = async (accountId, orderData) => {
    try {
      const newOrder = await tradingApi.createOrder(accountId, orderData);
      setOrders([newOrder, ...orders]);
      return newOrder;
    } catch (err) {
      throw new Error(err.message || 'Failed to create order');
    }
  };

  const cancelOrder = async (accountId, orderId) => {
    try {
      await tradingApi.cancelOrder(accountId, orderId);
      setOrders(orders.map(order => 
        order.id === orderId ? { ...order, status: 'cancelled' } : order
      ));
    } catch (err) {
      throw new Error(err.message || 'Failed to cancel order');
    }
  };

  const closePosition = async (accountId, positionId) => {
    try {
      await tradingApi.closePosition(accountId, positionId);
      setPositions(positions.filter(position => position.id !== positionId));
    } catch (err) {
      throw new Error(err.message || 'Failed to close position');
    }
  };

  return {
    accounts,
    positions,
    orders,
    loading,
    error,
    fetchAccounts,
    fetchPositions,
    fetchOrders,
    createOrder,
    cancelOrder,
    closePosition,
  };
}

