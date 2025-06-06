import { useState, useEffect } from 'react';
import { backtestsApi } from '@/lib/api';

export function useBacktests() {
  const [backtests, setBacktests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBacktests = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await backtestsApi.getAll();
      setBacktests(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch backtests');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBacktests();
  }, []);

  const createBacktest = async (backtestData) => {
    try {
      const newBacktest = await backtestsApi.create(backtestData);
      setBacktests([...backtests, newBacktest]);
      return newBacktest;
    } catch (err) {
      throw new Error(err.message || 'Failed to create backtest');
    }
  };

  const runBacktest = async (id) => {
    try {
      const results = await backtestsApi.run(id);
      setBacktests(
        backtests.map((backtest) =>
          backtest.id === id ? { ...backtest, results, status: 'completed' } : backtest
        )
      );
      return results;
    } catch (err) {
      setBacktests(
        backtests.map((backtest) =>
          backtest.id === id ? { ...backtest, status: 'failed' } : backtest
        )
      );
      throw new Error(err.message || 'Failed to run backtest');
    }
  };

  const getBacktestResults = async (id) => {
    try {
      return await backtestsApi.getResults(id);
    } catch (err) {
      throw new Error(err.message || 'Failed to get backtest results');
    }
  };

  const deleteBacktest = async (id) => {
    try {
      await backtestsApi.delete(id);
      setBacktests(backtests.filter((backtest) => backtest.id !== id));
    } catch (err) {
      throw new Error(err.message || 'Failed to delete backtest');
    }
  };

  return {
    backtests,
    loading,
    error,
    fetchBacktests,
    createBacktest,
    runBacktest,
    getBacktestResults,
    deleteBacktest,
    getReportUrl: backtestsApi.getReportUrl,
  };
}

