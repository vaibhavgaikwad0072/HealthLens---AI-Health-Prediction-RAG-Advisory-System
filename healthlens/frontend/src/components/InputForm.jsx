import React from 'react';
import { motion } from 'framer-motion';
import { Activity, Heart, Droplet, Clock, Info, Smartphone } from 'lucide-react';

export default function InputForm({ formData, setFormData, onPredict, onSync, loading }) {
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) || e.target.value });
  };

  const fields = [
    { name: 'age', label: 'Age (Yrs)', icon: <Info size={18}/> },
    { name: 'bmi', label: 'BMI', icon: <Activity size={18}/> },
    { name: 'heart_rate', label: 'Heart Rate (bpm)', icon: <Heart size={18}/> },
    { name: 'glucose', label: 'Glucose (mg/dL)', icon: <Droplet size={18}/> },
    { name: 'steps', label: 'Daily Steps', icon: <Activity size={18}/> },
    { name: 'sleep_hours', label: 'Sleep (Hrs)', icon: <Clock size={18}/> },
  ];

  return (
    <motion.div 
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className="bg-white p-6 rounded-2xl shadow-xl border border-gray-100"
    >
      <div className="flex items-center justify-between mb-6 border-b border-gray-100 pb-4">
        <h2 className="text-xl font-bold text-gray-800">Health Metrics</h2>
        <button 
          type="button" 
          onClick={onSync}
          className="flex items-center gap-2 text-sm font-semibold text-indigo-600 bg-indigo-50 px-4 py-2 rounded-xl hover:bg-indigo-100 transition-colors"
        >
          <Smartphone size={16} /> Sync Watch
        </button>
      </div>

      <form onSubmit={onPredict} className="space-y-5">
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-1 gap-4">
          {fields.map((field) => (
            <div key={field.name}>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                <span className="text-blue-500">{field.icon}</span>
                {field.label}
              </label>
              <input
                type="number"
                step="any"
                name={field.name}
                value={formData[field.name]}
                onChange={handleChange}
                className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all outline-none shadow-sm"
                required
              />
            </div>
          ))}
        </div>

        <button 
          type="submit" 
          disabled={loading}
          className="w-full mt-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold py-4 rounded-xl shadow-lg hover:shadow-xl hover:from-blue-700 hover:to-indigo-700 transition-all transform hover:-translate-y-0.5 disabled:opacity-70 disabled:transform-none"
        >
          {loading ? 'Analyzing Networks...' : 'Predict Disease Risk'}
        </button>
      </form>
    </motion.div>
  );
}
