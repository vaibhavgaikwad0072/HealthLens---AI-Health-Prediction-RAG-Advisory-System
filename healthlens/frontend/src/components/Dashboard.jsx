import React from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import RiskCard from './RiskCard';

export default function Dashboard({ risks, trendData }) {
  return (
    <div className="space-y-8">
      <h2 className="text-2xl font-extrabold text-gray-900 tracking-tight">Predictive Diagnostics</h2>
      
      {risks ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <RiskCard 
            title="Heart Disease" 
            riskPct={risks.heart_risk} 
            level={risks.risk_level.heart} 
            icon="❤️" 
          />
          <RiskCard 
            title="Diabetes Type II" 
            riskPct={risks.diabetes_risk} 
            level={risks.risk_level.diabetes} 
            icon="🍬" 
          />
          <RiskCard 
            title="Hypertension" 
            riskPct={risks.hypertension_risk || risks.cardio_risk} 
            level={risks.risk_level.cardio || risks.risk_level.hypertension} 
            icon="🩸" 
          />
        </div>
      ) : (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white rounded-3xl p-10 border-2 border-dashed border-gray-200 flex flex-col items-center justify-center text-center shadow-sm min-h-[200px]"
        >
          <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
            <span className="text-3xl opacity-50">📊</span>
          </div>
          <p className="text-gray-500 font-medium text-lg">Enter your metrics and click Predict to view your diagnostic status.</p>
          <p className="text-gray-400 text-sm mt-2">AI models will analyze your vitals securely.</p>
        </motion.div>
      )}

      <motion.div 
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1, duration: 0.4 }}
        className="bg-white shadow-xl rounded-3xl p-8 border border-gray-100 relative overflow-hidden"
      >
        <div className="absolute top-0 right-0 w-64 h-64 bg-blue-50 rounded-full mix-blend-multiply filter blur-3xl opacity-50 translate-x-1/2 -translate-y-1/2 pointer-events-none"></div>
        
        <h2 className="text-xl font-bold text-gray-800 mb-8 relative z-10">Prognostic Risk Trends</h2>
        <div className="h-[320px] relative z-10 w-full ml-[-15px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trendData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="4 4" vertical={false} stroke="#E5E7EB" />
              <XAxis dataKey="name" tick={{fontSize: 13, fill: '#9CA3AF', fontWeight: 500}} tickLine={false} axisLine={false} tickMargin={12} />
              <YAxis tick={{fontSize: 13, fill: '#9CA3AF', fontWeight: 500}} tickLine={false} axisLine={false} tickMargin={12} />
              <Tooltip 
                contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1)', padding: '12px 16px', fontWeight: 'bold' }} 
                itemStyle={{ fontSize: '14px', fontWeight: 600, padding: '4px 0' }}
              />
              <Legend iconType="circle" wrapperStyle={{ paddingTop: '24px', fontSize: '14px', fontWeight: 500 }} />
              <Line type="monotone" name="Heart" dataKey="heart_risk" stroke="#ef4444" strokeWidth={4} dot={{r: 5, strokeWidth: 2}} activeDot={{r: 8, strokeWidth: 0}} animationDuration={1500} />
              <Line type="monotone" name="Diabetes" dataKey="diabetes_risk" stroke="#f59e0b" strokeWidth={4} dot={{r: 5, strokeWidth: 2}} activeDot={{r: 8, strokeWidth: 0}} animationDuration={1500} />
              <Line type="monotone" name="Hypertension" dataKey="hypertension_risk" stroke="#0ea5e9" strokeWidth={4} dot={{r: 5, strokeWidth: 2}} activeDot={{r: 8, strokeWidth: 0}} animationDuration={1500} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </motion.div>
    </div>
  );
}
