import React, { useState } from 'react';

const difficultyColors = {
  easy: 'bg-green-100 text-green-700',
  medium: 'bg-amber-100 text-amber-700',
  hard: 'bg-red-100 text-red-700',
};

const categoryColors = {
  transport: 'bg-blue-100 text-blue-700',
  energy: 'bg-amber-100 text-amber-700',
  diet: 'bg-green-100 text-green-700',
  consumption: 'bg-purple-100 text-purple-700',
};

export default function RecommendationCard({ recommendation, onAct }) {
  const [expanded, setExpanded] = useState(false);
  const rec = recommendation;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h4 className="font-semibold text-gray-800">{rec.title}</h4>
          <div className="flex items-center gap-2 mt-1.5">
            <span className={`text-xs px-2 py-0.5 rounded font-medium ${categoryColors[rec.category] || 'bg-gray-100'}`}>
              {rec.category}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded font-medium ${difficultyColors[rec.difficulty] || 'bg-gray-100'}`}>
              {rec.difficulty}
            </span>
            <span className="text-xs text-gray-400">
              Save up to {rec.potential_co2_saved_kg} kg CO2/week
            </span>
          </div>
        </div>
        {rec.score && (
          <span className="text-sm font-medium text-eco-600 bg-eco-50 px-2 py-1 rounded">
            {(rec.score * 100).toFixed(0)}%
          </span>
        )}
      </div>

      <p className="text-sm text-gray-600 mb-3">{rec.description}</p>

      <button
        onClick={() => setExpanded(!expanded)}
        className="text-sm text-eco-600 hover:text-eco-700 font-medium mb-3"
      >
        {expanded ? 'Hide details' : 'Why this matters (MAO)'}
      </button>

      {expanded && (
        <div className="space-y-3 mb-4 bg-gray-50 rounded-lg p-4">
          {rec.mao_motivation && (
            <div>
              <h5 className="text-xs font-semibold text-gray-500 uppercase mb-1">Motivation</h5>
              <p className="text-sm text-gray-600">{rec.mao_motivation}</p>
            </div>
          )}
          {rec.mao_ability && (
            <div>
              <h5 className="text-xs font-semibold text-gray-500 uppercase mb-1">Ability</h5>
              <p className="text-sm text-gray-600">{rec.mao_ability}</p>
            </div>
          )}
          {rec.mao_opportunity && (
            <div>
              <h5 className="text-xs font-semibold text-gray-500 uppercase mb-1">Opportunity</h5>
              <p className="text-sm text-gray-600">{rec.mao_opportunity}</p>
            </div>
          )}
        </div>
      )}

      <div className="flex gap-2">
        <button
          onClick={() => onAct(rec.id, 'accepted')}
          className="flex-1 bg-eco-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-eco-700 transition"
        >
          Accept
        </button>
        <button
          onClick={() => onAct(rec.id, 'dismissed')}
          className="flex-1 bg-gray-100 text-gray-600 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition"
        >
          Dismiss
        </button>
      </div>
    </div>
  );
}
