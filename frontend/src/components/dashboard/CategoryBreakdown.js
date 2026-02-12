import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import Card from '../common/Card';

const COLORS = {
  transport: '#3b82f6',
  energy: '#f59e0b',
  diet: '#22c55e',
  consumption: '#a855f7',
};

export default function CategoryBreakdown({ categories }) {
  const data = Object.entries(categories || {}).map(([key, val]) => ({
    name: key.charAt(0).toUpperCase() + key.slice(1),
    value: val.total_co2_kg || 0,
  })).filter(d => d.value > 0);

  return (
    <Card title="Category Breakdown">
      {data.length > 0 ? (
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={100}
              paddingAngle={3}
              dataKey="value"
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            >
              {data.map((entry) => (
                <Cell key={entry.name} fill={COLORS[entry.name.toLowerCase()] || '#94a3b8'} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value.toFixed(2)} kg CO2`} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      ) : (
        <div className="h-64 flex items-center justify-center text-gray-400">
          No activities logged for this period.
        </div>
      )}
    </Card>
  );
}
