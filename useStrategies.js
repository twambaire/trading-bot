import { useState, useEffect } from 'react';
import { strategiesApi } from '@/lib/api';

export function useStrategies() {
  const [strategies, setStrategies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStrategies = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await strategiesApi.getAll();
      setStrategies(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch strategies');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStrategies();
  }, []);

  const createStrategy = async (strategyData) => {
    try {
      const newStrategy = await strategiesApi.create(strategyData);
      setStrategies([...strategies, newStrategy]);
      return newStrategy;
    } catch (err) {
      throw new Error(err.message || 'Failed to create strategy');
    }
  };

  const updateStrategy = async (id, strategyData) => {
    try {
      const updatedStrategy = await strategiesApi.update(id, strategyData);
      setStrategies(
        strategies.map((strategy) =>
          strategy.id === id ? updatedStrategy : strategy
        )
      );
      return updatedStrategy;
    } catch (err) {
      throw new Error(err.message || 'Failed to update strategy');
    }
  };

  const deleteStrategy = async (id) => {
    try {
      await strategiesApi.delete(id);
      setStrategies(strategies.filter((strategy) => strategy.id !== id));
    } catch (err) {
      throw new Error(err.message || 'Failed to delete strategy');
    }
  };

  return {
    strategies,
    loading,
    error,
    fetchStrategies,
    createStrategy,
    updateStrategy,
    deleteStrategy,
  };
}

