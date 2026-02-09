import React, { useState, useEffect } from 'react';
import client from '../api/client';
import WeeklySummary from '../components/dashboard/WeeklySummary';
import FootprintChart from '../components/dashboard/FootprintChart';
import CategoryBreakdown from '../components/dashboard/CategoryBreakdown';
import PredictionCard from '../components/dashboard/PredictionCard';

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [trend, setTrend] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [period, setPeriod] = useState('week');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [summaryRes, trendRes, predRes] = await Promise.all([
          client.get(`/dashboard/summary?period=${period}`),
          client.get('/dashboard/trend?weeks=12'),
          client.get('/dashboard/prediction'),
        ]);
        setSummary(summaryRes.data);
        setTrend(trendRes.data.trend);
        setPrediction(predRes.data);
      } catch (err) {
        console.error('Dashboard fetch error:', err);
      }
    };
    fetchData();
  }, [period]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <select
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-eco-500 outline-none"
        >
          <option value="week">This Week</option>
          <option value="month">This Month</option>
          <option value="year">This Year</option>
        </select>
      </div>

      <WeeklySummary summary={summary} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <FootprintChart data={trend} />
        </div>
        <div className="space-y-6">
          <CategoryBreakdown categories={summary?.categories} />
          <PredictionCard prediction={prediction} />
        </div>
      </div>
    </div>
  );
}
