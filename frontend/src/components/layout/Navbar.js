import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-eco-700 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/dashboard" className="text-xl font-bold">
              EcoTrack
            </Link>
          </div>
          <div className="hidden md:flex items-center space-x-4">
            <Link to="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-eco-600 transition">
              Dashboard
            </Link>
            <Link to="/activities" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-eco-600 transition">
              Activities
            </Link>
            <Link to="/goals" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-eco-600 transition">
              Goals
            </Link>
            <Link to="/recommendations" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-eco-600 transition">
              Recommendations
            </Link>
            <Link to="/emission-factors" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-eco-600 transition">
              Emission Factors
            </Link>
          </div>
          <div className="flex items-center space-x-3">
            <Link to="/profile" className="text-sm hover:underline">
              {user?.display_name}
            </Link>
            <button
              onClick={logout}
              className="bg-eco-800 px-3 py-1.5 rounded text-sm hover:bg-eco-900 transition"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
