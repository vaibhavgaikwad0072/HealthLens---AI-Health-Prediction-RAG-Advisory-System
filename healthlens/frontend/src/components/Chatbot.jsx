import React, { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, Bot, User } from 'lucide-react';

export default function Chatbot({ chatQuery, setChatQuery, sendQuery, chatHistory }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  return (
    <motion.div 
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="bg-white shadow-2xl rounded-2xl border border-gray-100 flex flex-col h-[750px] overflow-hidden"
    >
      <div className="p-6 bg-gradient-to-r from-teal-600 to-blue-700 text-white flex items-center gap-4 shadow-md relative z-10">
        <div className="bg-white/20 p-2.5 rounded-xl backdrop-blur-md border border-white/10 shadow-inner">
          <Bot size={28} className="text-white" />
        </div>
        <div>
          <h2 className="text-xl font-bold leading-tight tracking-wide">AI Health Advisor</h2>
          <p className="text-sm text-teal-100 opacity-90 font-medium tracking-wider">WHO Guidelines FAISS-RAG</p>
        </div>
      </div>

      <div className="flex-1 p-5 overflow-y-auto bg-[#f8fafc] flex flex-col space-y-5 custom-scrollbar">
        {chatHistory.length === 0 ? (
          <div className="m-auto text-center px-8 flex flex-col items-center justify-center opacity-80">
            <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-5">
              <Bot size={40} className="text-gray-400" />
            </div>
            <p className="text-gray-700 font-semibold text-lg">Hello there! I'm your digital health AI.</p>
            <p className="text-sm text-gray-500 mt-2 leading-relaxed">Ask me anything about managing diet, lifestyle, and risks based on the latest medical literature.</p>
          </div>
        ) : (
          chatHistory.map((msg, idx) => (
            <motion.div 
              initial={{ opacity: 0, y: 10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.2 }}
              key={idx} 
              className={`flex items-end gap-3 max-w-[85%] ${msg.type === 'user' ? 'ml-auto flex-row-reverse' : ''}`}
            >
              <div className={`p-2.5 rounded-full flex-shrink-0 shadow-sm ${msg.type === 'user' ? 'bg-blue-100 text-blue-700' : 'bg-teal-100 text-teal-700'}`}>
                {msg.type === 'user' ? <User size={18}/> : <Bot size={18}/>}
              </div>
              <div className={`py-3.5 px-5 rounded-2xl text-[15px] leading-relaxed shadow-sm ${msg.type === 'user' ? 'bg-blue-600 text-white rounded-tr-sm' : 'bg-white border border-gray-100 text-gray-800 rounded-tl-sm'}`}>
                {msg.text}
              </div>
            </motion.div>
          ))
        )}
        <div ref={endRef} />
      </div>

      <div className="p-5 bg-white border-t border-gray-100 z-10 shadow-[0_-10px_15px_-3px_rgba(0,0,0,0.02)]">
        <div className="flex gap-3">
          <input 
            type="text" 
            value={chatQuery} 
            onChange={(e) => setChatQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendQuery()}
            placeholder="Type your health query..." 
            className="flex-1 bg-gray-50 border border-gray-200 p-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-500 focus:bg-white text-[15px] transition-all shadow-inner"
          />
          <button 
            onClick={sendQuery} 
            className="bg-teal-600 text-white p-4 rounded-xl hover:bg-teal-700 transition-all shadow-md hover:shadow-lg flex items-center justify-center w-16 transform hover:-translate-y-0.5 active:translate-y-0"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </motion.div>
  );
}
