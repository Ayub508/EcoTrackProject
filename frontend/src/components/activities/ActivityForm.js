import React, { useState } from 'react';
import client from '../../api/client';

const SUB_CATEGORIES = {
  transport: [
    { value: 'car_petrol', label: 'Car (Petrol)', unit: 'km' },
    { value: 'car_diesel', label: 'Car (Diesel)', unit: 'km' },
    { value: 'car_electric', label: 'Car (Electric)', unit: 'km' },
    { value: 'car_hybrid', label: 'Car (Hybrid)', unit: 'km' },
    { value: 'bus', label: 'Bus', unit: 'km' },
    { value: 'train', label: 'Train', unit: 'km' },
    { value: 'domestic_flight', label: 'Domestic Flight', unit: 'km' },
    { value: 'short_haul_flight', label: 'Short-haul Flight', unit: 'km' },
    { value: 'long_haul_flight', label: 'Long-haul Flight', unit: 'km' },
    { value: 'bicycle', label: 'Bicycle', unit: 'km' },
    { value: 'walking', label: 'Walking', unit: 'km' },
  ],
  energy: [
    { value: 'electricity_uk', label: 'Electricity (UK)', unit: 'kWh' },
    { value: 'electricity_us', label: 'Electricity (US)', unit: 'kWh' },
    { value: 'natural_gas', label: 'Natural Gas', unit: 'm³' },
    { value: 'heating_oil', label: 'Heating Oil', unit: 'litres' },
    { value: 'solar_panel', label: 'Solar Panel', unit: 'kWh' },
  ],
  diet: [
    { value: 'beef', label: 'Beef', unit: 'kg' },
    { value: 'lamb', label: 'Lamb', unit: 'kg' },
    { value: 'pork', label: 'Pork', unit: 'kg' },
    { value: 'chicken', label: 'Chicken', unit: 'kg' },
    { value: 'fish', label: 'Fish', unit: 'kg' },
    { value: 'cheese', label: 'Cheese', unit: 'kg' },
    { value: 'milk', label: 'Milk', unit: 'litres' },
    { value: 'eggs', label: 'Eggs', unit: 'kg' },
    { value: 'rice', label: 'Rice', unit: 'kg' },
    { value: 'vegetables', label: 'Vegetables', unit: 'kg' },
    { value: 'fruits', label: 'Fruits', unit: 'kg' },
    { value: 'tofu', label: 'Tofu', unit: 'kg' },
  ],
  consumption: [
    { value: 'clothing_new', label: 'New Clothing', unit: 'items' },
    { value: 'clothing_secondhand', label: 'Secondhand Clothing', unit: 'items' },
    { value: 'smartphone', label: 'Smartphone', unit: 'items' },
    { value: 'laptop', label: 'Laptop', unit: 'items' },
    { value: 'plastic_bag', label: 'Plastic Bags', unit: 'items' },
    { value: 'furniture_wooden', label: 'Wooden Furniture', unit: 'items' },
    { value: 'streaming_video', label: 'Video Streaming', unit: 'hours' },
  ],
};

export default function ActivityForm({ onSuccess }) {
  const [activeTab, setActiveTab] = useState('transport');
  const [subCategory, setSubCategory] = useState('');
  const [quantity, setQuantity] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const currentSubs = SUB_CATEGORIES[activeTab] || [];
  const selectedSub = currentSubs.find(s => s.value === subCategory);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await client.post('/activities', {
        category: activeTab,
        sub_category: subCategory,
        quantity: parseFloat(quantity),
        unit: selectedSub?.unit || 'unit',
        date,
        notes: notes || null,
      });
      setSubCategory('');
      setQuantity('');
      setNotes('');
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to log activity');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { key: 'transport', label: 'Transport' },
    { key: 'energy', label: 'Energy' },
    { key: 'diet', label: 'Diet' },
    { key: 'consumption', label: 'Consumption' },
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Log Activity</h3>

      <div className="flex space-x-1 bg-gray-100 rounded-lg p-1 mb-4">
        {tabs.map(tab => (
          <button
            key={tab.key}
            onClick={() => { setActiveTab(tab.key); setSubCategory(''); }}
            className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition ${
              activeTab === tab.key
                ? 'bg-white text-eco-700 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-2 rounded-lg mb-4 text-sm">{error}</div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Activity Type</label>
          <select
            value={subCategory}
            onChange={(e) => setSubCategory(e.target.value)}
            required
            className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
          >
            <option value="">Select type...</option>
            {currentSubs.map(sub => (
              <option key={sub.value} value={sub.value}>{sub.label}</option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Quantity {selectedSub && `(${selectedSub.unit})`}
            </label>
            <input
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              required
              min="0"
              step="0.01"
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
              placeholder="0.00"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Notes (optional)</label>
          <input
            type="text"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-eco-500 outline-none"
            placeholder="E.g., commute to work"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-eco-600 text-white py-2.5 rounded-lg font-medium hover:bg-eco-700 transition disabled:opacity-50"
        >
          {loading ? 'Logging...' : 'Log Activity'}
        </button>
      </form>
    </div>
  );
}
