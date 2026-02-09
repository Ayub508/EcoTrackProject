import React, { useState, useEffect } from 'react';
import client from '../api/client';
import RecommendationCard from '../components/recommendations/RecommendationCard';

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState([]);
  const [behaviourClass, setBehaviourClass] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchRecommendations = async () => {
    try {
      const res = await client.get('/recommendations');
      setRecommendations(res.data.recommendations || []);
      setBehaviourClass(res.data.behaviour_class || '');
    } catch (err) {
      console.error('Failed to fetch recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchRecommendations(); }, []);

  const handleAct = async (recId, action) => {
    try {
      await client.post(`/recommendations/${recId}/act`, { action });
      setRecommendations(prev => prev.filter(r => r.id !== recId));
    } catch (err) {
      console.error('Failed to act on recommendation:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-eco-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Recommendations</h1>
          {behaviourClass && (
            <p className="text-sm text-gray-500 mt-1">
              Your profile: <span className="font-medium text-eco-600">{behaviourClass.replace(/_/g, ' ')}</span>
            </p>
          )}
        </div>
      </div>

      {recommendations.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recommendations.map(rec => (
            <RecommendationCard key={rec.id} recommendation={rec} onAct={handleAct} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-400">
          <p className="text-lg">No recommendations available</p>
          <p className="text-sm mt-1">Log more activities to get personalised tips</p>
        </div>
      )}
    </div>
  );
}
