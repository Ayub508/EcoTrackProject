import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import Card from '../common/Card';

export default function FootprintChart({ data }) {
  return (
    <Card title="Carbon Footprint Trend">
      {data && data.length > 0 ? (
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="week" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} label={{ value: 'kg CO2', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Area type="monotone" dataKey="transport" stackId="1" stroke="#3b82f6" fill="#93c5fd" name="Transport" />
            <Area type="monotone" dataKey="energy" stackId="1" stroke="#f59e0b" fill="#fcd34d" name="Energy" />
            <Area type="monotone" dataKey="diet" stackId="1" stroke="#22c55e" fill="#86efac" name="Diet" />
            <Area type="monotone" dataKey="consumption" stackId="1" stroke="#a855f7" fill="#d8b4fe" name="Consumption" />
          </AreaChart>
        </ResponsiveContainer>
      ) : (
        <div className="h-64 flex items-center justify-center text-gray-400">
          No data yet. Start logging activities to see trends.
        </div>
      )}
    </Card>
  );
}
