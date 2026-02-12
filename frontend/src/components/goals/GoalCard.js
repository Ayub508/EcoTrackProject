import React from 'react';

const statusColors = {
  active: 'bg-eco-100 text-eco-700',
  achieved: 'bg-green-100 text-green-700',
  missed: 'bg-red-100 text-red-700',
};

export default function GoalCard({ goal, onDelete }) {
  const progressPct = Math.min(goal.progress || 0, 100);
  const isOverTarget = goal.current_co2_kg > goal.target_co2_kg;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h4 className="font-semibold text-gray-800">{goal.title}</h4>
          <div className="flex items-center gap-2 mt-1">
            {goal.category && (
              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded">
                {goal.category}
              </span>
            )}
            <span className={`text-xs px-2 py-0.5 rounded font-medium ${statusColors[goal.status] || 'bg-gray-100 text-gray-600'}`}>
              {goal.status}
            </span>
          </div>
        </div>
        <button
          onClick={() => onDelete(goal.id)}
          className="text-gray-400 hover:text-red-500 transition"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div className="mb-2">
        <div className="flex justify-between text-sm mb-1">
          <span className="text-gray-500">
            {goal.current_co2_kg} / {goal.target_co2_kg} kg CO2
          </span>
          <span className={`font-medium ${isOverTarget ? 'text-red-500' : 'text-eco-600'}`}>
            {progressPct.toFixed(0)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className={`h-2.5 rounded-full transition-all ${isOverTarget ? 'bg-red-400' : 'bg-eco-500'}`}
            style={{ width: `${Math.min(progressPct, 100)}%` }}
          ></div>
        </div>
      </div>

      <div className="flex justify-between text-xs text-gray-400 mt-2">
        <span>{goal.period}</span>
        <span>{goal.start_date} {goal.end_date ? `- ${goal.end_date}` : ''}</span>
      </div>
    </div>
  );
}
