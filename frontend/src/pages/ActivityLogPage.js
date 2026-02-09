import React, { useState, useEffect, useCallback } from 'react';
import client from '../api/client';
import ActivityForm from '../components/activities/ActivityForm';
import ActivityHistory from '../components/activities/ActivityHistory';

export default function ActivityLogPage() {
  const [activities, setActivities] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [categoryFilter, setCategoryFilter] = useState('');

  const fetchActivities = useCallback(async () => {
    try {
      const params = { page, per_page: 15 };
      if (categoryFilter) params.category = categoryFilter;
      const res = await client.get('/activities', { params });
      setActivities(res.data.activities);
      setTotalPages(res.data.pages);
    } catch (err) {
      console.error('Failed to fetch activities:', err);
    }
  }, [page, categoryFilter]);

  useEffect(() => {
    fetchActivities();
  }, [fetchActivities]);

  const handleDelete = async (id) => {
    try {
      await client.delete(`/activities/${id}`);
      fetchActivities();
    } catch (err) {
      console.error('Failed to delete activity:', err);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Activity Log</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <ActivityForm onSuccess={fetchActivities} />
        </div>
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center gap-3">
            <select
              value={categoryFilter}
              onChange={(e) => { setCategoryFilter(e.target.value); setPage(1); }}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-eco-500 outline-none"
            >
              <option value="">All Categories</option>
              <option value="transport">Transport</option>
              <option value="energy">Energy</option>
              <option value="diet">Diet</option>
              <option value="consumption">Consumption</option>
            </select>
          </div>

          <ActivityHistory activities={activities} onDelete={handleDelete} />

          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-3 py-1.5 border rounded text-sm disabled:opacity-50"
              >
                Previous
              </button>
              <span className="text-sm text-gray-500">Page {page} of {totalPages}</span>
              <button
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="px-3 py-1.5 border rounded text-sm disabled:opacity-50"
              >
                Next
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
