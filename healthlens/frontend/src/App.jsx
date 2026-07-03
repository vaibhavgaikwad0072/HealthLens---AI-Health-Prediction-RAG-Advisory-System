import React, { useState } from 'react';
import axios from 'axios';
import { Activity } from 'lucide-react';
import InputForm from './components/InputForm';
import Dashboard from './components/Dashboard';
import Chatbot from './components/Chatbot';

function App() {
  const [formData, setFormData] = useState({
    age: 42, bmi: 26.5, heart_rate: 74, glucose: 95.0, steps: 4800, sleep_hours: 6.5
  });
  const [risks, setRisks] = useState(null);
  const [chatQuery, setChatQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // Hardcoded trend data simulating DB output
  const trendData = [
    { name: 'Jan', heart_risk: 45, diabetes_risk: 30, hypertension_risk: 60 },
    { name: 'Feb', heart_risk: 42, diabetes_risk: 32, hypertension_risk: 58 },
    { name: 'Mar', heart_risk: 38, diabetes_risk: 28, hypertension_risk: 55 },
    { name: 'Apr', heart_risk: 35, diabetes_risk: 26, hypertension_risk: 52 },
    { name: 'May', heart_risk: 34, diabetes_risk: 24, hypertension_risk: 49 },
    { name: 'Jun', heart_risk: 31, diabetes_risk: 22, hypertension_risk: 47 }
  ];

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/api/predict/all', formData);
      setRisks(res.data);
      if (res.data.recommendation) {
        setChatHistory([{ type: 'bot', text: res.data.recommendation }]);
      }
    } catch (err) {
      console.error(err);
      alert("Prediction failed. Ensure ML models and Backend are up.");
    }
    setLoading(false);
  };

  const handleSync = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/user/health-data');
      setFormData((prev) => ({ ...prev, ...res.data }));
    } catch (err) {
      console.error(err);
      alert("Google Fit sync failed. Ensure backend is running.");
    }
  };

  const handleChat = async () => {
    if (!chatQuery.trim()) return;
    const newHistory = [...chatHistory, { type: 'user', text: chatQuery }];
    setChatHistory(newHistory);
    try {
      const res = await axios.post('http://localhost:8000/api/chat', { query: chatQuery });
      setChatHistory([...newHistory, { type: 'bot', text: res.data.response }]);
    } catch (err) {
      setChatHistory([...newHistory, { type: 'bot', text: "Error connecting to AI Advisor." }]);
    }
    setChatQuery("");
  };

  return (
    <div className="min-h-screen bg-[#f3f6f9] flex flex-col font-sans selection:bg-blue-200">
      <nav className="bg-white border-b border-gray-100 shadow-sm sticky top-0 z-50">
        <div className="max-w-[1600px] mx-auto px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-tr from-blue-600 to-indigo-500 p-2.5 rounded-xl shadow-md text-white border border-white/20">
              <Activity size={24} strokeWidth={2.5} />
            </div>
            <div>
              <h1 className="text-2xl font-black text-gray-900 tracking-tight">HealthLens</h1>
              <p className="text-[10px] uppercase font-bold text-blue-500 tracking-[0.2em] mt-0.5">AI Risk Predictor</p>
            </div>
          </div>
          <div className="flex items-center gap-5">
            <span className="text-sm font-semibold text-gray-500 hidden sm:block">Welcome, Alex</span>
            <div className="w-11 h-11 rounded-full bg-gradient-to-tr from-blue-50 to-indigo-50 border-2 border-blue-200 flex items-center justify-center text-blue-700 font-bold shadow-inner cursor-pointer hover:shadow-md transition">
              A
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-[1600px] mx-auto w-full px-4 sm:px-8 py-10 flex-1 grid grid-cols-1 xl:grid-cols-12 gap-8">
        
        {/* Left Col: Input Forms */}
        <div className="xl:col-span-3">
          <InputForm 
            formData={formData} 
            setFormData={setFormData} 
            onPredict={handlePredict} 
            onSync={handleSync} 
            loading={loading} 
          />
        </div>

        {/* Center Col: Dashboard Metrics & Charts */}
        <div className="xl:col-span-5">
          <Dashboard risks={risks} trendData={trendData} />
        </div>

        {/* Right Col: Companion Chatbot */}
        <div className="xl:col-span-4">
          <Chatbot 
            chatQuery={chatQuery} 
            setChatQuery={setChatQuery} 
            sendQuery={handleChat} 
            chatHistory={chatHistory} 
          />
        </div>

      </main>
    </div>
  );
}

export default App;
