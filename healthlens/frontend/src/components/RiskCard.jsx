import React from 'react';
import { motion } from 'framer-motion';

export default function RiskCard({ title, riskPct, level, icon }) {
  const getColor = (lvl) => {
    if (lvl === 'High') return { bg: 'bg-red-50', text: 'text-red-600', bar: 'bg-red-500', shadow: 'shadow-red-50' };
    if (lvl === 'Medium') return { bg: 'bg-yellow-50', text: 'text-yellow-600', bar: 'bg-yellow-500', shadow: 'shadow-yellow-50' };
    return { bg: 'bg-green-50', text: 'text-green-600', bar: 'bg-green-500', shadow: 'shadow-green-50' };
  };

  const colors = getColor(level || 'Low');

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -4, boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)' }}
      className={`relative p-6 rounded-2xl bg-white border border-gray-100 shadow-lg ${colors.shadow} overflow-hidden`}
    >
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-gray-600 font-semibold">{title}</h3>
        <span className="text-2xl">{icon}</span>
      </div>
      
      <div className="flex items-end gap-3 mb-5">
        <span className={`text-4xl font-extrabold tracking-tight ${colors.text}`}>
          {riskPct ?? 0}%
        </span>
        <span className={`px-3 py-1 text-xs font-bold uppercase rounded-full ${colors.bg} ${colors.text}`}>
          {level || 'Normal'}
        </span>
      </div>

      <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: `${riskPct ?? 0}%` }}
          transition={{ duration: 1, ease: 'easeOut' }}
          className={`h-3 rounded-full ${colors.bar}`}
        />
      </div>
    </motion.div>
  );
}
