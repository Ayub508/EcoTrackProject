import React, { useState, useEffect } from 'react';
import client from '../api/client';

export default function EmissionFactorsPage() {
  const [factors, setFactors] = useState([]);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFactors = async () => {
      try {
        const params = {};
        if (categoryFilter) params.category = categoryFilter;
        if (search) params.search = search;
        const res = await client.get('/emission-factors', { params });
        setFactors(res.data.emission_factors);
      } catch (err) {
        console.error('Failed to fetch emission factors:', err);
      } finally {
        setLoading(false);
      }
    };

    const debounce = setTimeout(fetchFactors, 300);
    return () => clearTimeout(debounce);
  }, [search, categoryFilter]);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Emission Factors</h1>
          <p className="text-sm text-gray-500 mt-1">
            Transparent emission factors from trusted sources
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search emission factors..."
            className="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
          />
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
          >
            <option value="">All Categories</option>
            <option value="transport">Transport</option>
            <option value="energy">Energy</option>
            <option value="diet">Diet</option>
            <option value="consumption">Consumption</option>
          </select>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-eco-600 mx-auto"></div>
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Category</th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Sub-category</th>
                    <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 uppercase">Factor</th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Unit</th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Source</th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Region</th>
                    <th className="text-center px-6 py-3 text-xs font-medium text-gray-500 uppercase">Year</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {factors.map((factor) => (
                    <tr key={factor.id} className="hover:bg-gray-50 transition">
                      <td className="px-6 py-4 text-sm text-gray-600 capitalize">{factor.category}</td>
                      <td className="px-6 py-4 text-sm text-gray-800">{factor.sub_category.replace(/_/g, ' ')}</td>
                      <td className="px-6 py-4 text-sm font-medium text-gray-800 text-right">{factor.factor_value}</td>
                      <td className="px-6 py-4 text-sm text-gray-500">{factor.unit}</td>
                      <td className="px-6 py-4 text-sm">
                        {factor.source_url ? (
                          <a href={factor.source_url} target="_blank" rel="noopener noreferrer"
                            className="text-eco-600 hover:underline">{factor.source}</a>
                        ) : (
                          <span className="text-gray-600">{factor.source}</span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">{factor.region}</td>
                      <td className="px-6 py-4 text-sm text-gray-500 text-center">{factor.year}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {factors.length === 0 && (
              <div className="text-center py-8 text-gray-400">No emission factors found.</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
