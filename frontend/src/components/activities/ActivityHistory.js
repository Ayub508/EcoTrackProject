import React from 'react';

const categoryColors = {
  transport: 'bg-blue-100 text-blue-700',
  energy: 'bg-amber-100 text-amber-700',
  diet: 'bg-green-100 text-green-700',
  consumption: 'bg-purple-100 text-purple-700',
};

export default function ActivityHistory({ activities, onDelete }) {
  if (!activities || activities.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center text-gray-400">
        No activities logged yet.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100">
        <h3 className="text-lg font-semibold text-gray-800">Activity History</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50">
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Date</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Category</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Type</th>
              <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 uppercase">Quantity</th>
              <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 uppercase">CO2 (kg)</th>
              <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {activities.map((activity) => (
              <tr key={activity.id} className="hover:bg-gray-50 transition">
                <td className="px-6 py-4 text-sm text-gray-600">{activity.date}</td>
                <td className="px-6 py-4">
                  <span className={`inline-block px-2.5 py-1 rounded-full text-xs font-medium ${categoryColors[activity.category] || 'bg-gray-100 text-gray-600'}`}>
                    {activity.category}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-800">
                  {activity.sub_category.replace(/_/g, ' ')}
                </td>
                <td className="px-6 py-4 text-sm text-gray-600 text-right">
                  {activity.quantity} {activity.unit}
                </td>
                <td className="px-6 py-4 text-sm font-medium text-gray-800 text-right">
                  {activity.co2_kg}
                </td>
                <td className="px-6 py-4 text-right">
                  <button
                    onClick={() => onDelete(activity.id)}
                    className="text-red-500 hover:text-red-700 text-sm transition"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
