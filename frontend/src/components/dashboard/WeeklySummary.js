import React from 'react';

const categoryIcons = {
  transport: { bg: 'bg-blue-50', text: 'text-blue-600', label: 'Transport' },
  energy: { bg: 'bg-amber-50', text: 'text-amber-600', label: 'Energy' },
  diet: { bg: 'bg-green-50', text: 'text-green-600', label: 'Diet' },
  consumption: { bg: 'bg-purple-50', text: 'text-purple-600', label: 'Consumption' },
};

export default function WeeklySummary({ summary }) {
  if (!summary) return null;

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
        <p className="text-sm text-gray-500">Total CO2</p>
        <p className="text-2xl font-bold text-gray-800 mt-1">
          {summary.total_co2_kg?.toFixed(1) || '0'} <span className="text-sm font-normal text-gray-400">kg</span>
        </p>
        <p className="text-xs text-gray-400 mt-1">This {summary.period}</p>
      </div>
      {Object.entries(summary.categories || {}).map(([key, val]) => {
        const style = categoryIcons[key] || categoryIcons.transport;
        return (
          <div key={key} className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <p className={`text-sm ${style.text}`}>{style.label}</p>
            <p className="text-2xl font-bold text-gray-800 mt-1">
              {val.total_co2_kg?.toFixed(1)} <span className="text-sm font-normal text-gray-400">kg</span>
            </p>
            <p className="text-xs text-gray-400 mt-1">{val.activity_count} activities</p>
          </div>
        );
      })}
    </div>
  );
}
