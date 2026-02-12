import React from 'react';
import Card from '../common/Card';

export default function PredictionCard({ prediction }) {
  return (
    <Card title="Predicted Next Period">
      {prediction?.predicted_co2_kg != null ? (
        <div className="text-center py-4">
          <p className="text-4xl font-bold text-eco-600">
            {prediction.predicted_co2_kg.toFixed(1)}
          </p>
          <p className="text-sm text-gray-500 mt-2">kg CO2 predicted</p>
          <p className="text-xs text-gray-400 mt-1">{prediction.message}</p>
        </div>
      ) : (
        <div className="text-center py-4 text-gray-400">
          <p className="text-sm">{prediction?.message || 'Not enough data for prediction'}</p>
          <p className="text-xs mt-1">Log activities for at least 4 weeks</p>
        </div>
      )}
    </Card>
  );
}
