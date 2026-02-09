import React, { useState, useEffect } from 'react';
import client from '../api/client';
import GoalCard from '../components/goals/GoalCard';
import Modal from '../components/common/Modal';

export default function GoalsPage() {
  const [goals, setGoals] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [statusFilter, setStatusFilter] = useState('active');
  const [form, setForm] = useState({
    title: '', category: '', target_co2_kg: '', period: 'weekly',
    start_date: new Date().toISOString().split('T')[0], end_date: ''
  });
  const [error, setError] = useState('');

  const fetchGoals = async () => {
    try {
      const res = await client.get(`/goals?status=${statusFilter}`);
      setGoals(res.data.goals);
    } catch (err) {
      console.error('Failed to fetch goals:', err);
    }
  };

  useEffect(() => { fetchGoals(); }, [statusFilter]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await client.post('/goals', {
        ...form,
        target_co2_kg: parseFloat(form.target_co2_kg),
        end_date: form.end_date || null,
        category: form.category || null,
      });
      setShowModal(false);
      setForm({ title: '', category: '', target_co2_kg: '', period: 'weekly',
        start_date: new Date().toISOString().split('T')[0], end_date: '' });
      fetchGoals();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create goal');
    }
  };

  const handleDelete = async (id) => {
    try {
      await client.delete(`/goals/${id}`);
      fetchGoals();
    } catch (err) {
      console.error('Failed to delete goal:', err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Goals</h1>
        <div className="flex items-center gap-3">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
          >
            <option value="active">Active</option>
            <option value="achieved">Achieved</option>
            <option value="missed">Missed</option>
            <option value="all">All</option>
          </select>
          <button
            onClick={() => setShowModal(true)}
            className="bg-eco-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-eco-700 transition"
          >
            New Goal
          </button>
        </div>
      </div>

      {goals.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {goals.map(goal => (
            <GoalCard key={goal.id} goal={goal} onDelete={handleDelete} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-400">
          <p className="text-lg">No goals yet</p>
          <p className="text-sm mt-1">Set a goal to start tracking your progress</p>
        </div>
      )}

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Create New Goal">
        {error && <div className="bg-red-50 text-red-600 px-4 py-2 rounded-lg mb-4 text-sm">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Goal Title</label>
            <input
              type="text" required value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
              placeholder="e.g., Reduce transport emissions"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Category (optional)</label>
              <select
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
              >
                <option value="">All categories</option>
                <option value="transport">Transport</option>
                <option value="energy">Energy</option>
                <option value="diet">Diet</option>
                <option value="consumption">Consumption</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Target (kg CO2)</label>
              <input
                type="number" required min="0" step="0.1" value={form.target_co2_kg}
                onChange={(e) => setForm({ ...form, target_co2_kg: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
              />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Period</label>
              <select
                value={form.period}
                onChange={(e) => setForm({ ...form, period: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input
                type="date" required value={form.start_date}
                onChange={(e) => setForm({ ...form, start_date: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
              <input
                type="date" value={form.end_date}
                onChange={(e) => setForm({ ...form, end_date: e.target.value })}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
              />
            </div>
          </div>
          <button
            type="submit"
            className="w-full bg-eco-600 text-white py-2.5 rounded-lg font-medium hover:bg-eco-700 transition"
          >
            Create Goal
          </button>
        </form>
      </Modal>
    </div>
  );
}
