import React, { useState } from 'react';
import { Sparkles } from 'lucide-react';

const CopilotForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    topic: '',
    level: 'Beginner',
    availableTime: '1-2 weeks',
    dailyStudyTime: '1 hour'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.topic.trim()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl border border-[#E8E7EF] shadow-sm">
      <h3 className="font-bold text-lg text-[#17152A] mb-4 flex items-center gap-2">
        <Sparkles className="w-5 h-5 text-[#6D4AFF]" />
        What do you want to learn?
      </h3>
      
      <div className="space-y-5">
        <div>
          <input 
            type="text" 
            placeholder="e.g. Computer Networking fundamentals..."
            className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#6D4AFF] focus:border-transparent transition-all"
            value={formData.topic}
            onChange={(e) => setFormData({...formData, topic: e.target.value})}
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-[#747184] mb-2">Current Level</label>
            <select 
              className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#6D4AFF]"
              value={formData.level}
              onChange={(e) => setFormData({...formData, level: e.target.value})}
            >
              <option>Beginner</option>
              <option>Intermediate</option>
              <option>Advanced</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-[#747184] mb-2">Available Time</label>
            <select 
              className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#6D4AFF]"
              value={formData.availableTime}
              onChange={(e) => setFormData({...formData, availableTime: e.target.value})}
            >
              <option>1–2 weeks</option>
              <option>3–4 weeks</option>
              <option>5–8 weeks</option>
              <option>Semester</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-[#747184] mb-2">Daily Study Time</label>
            <select 
              className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#6D4AFF]"
              value={formData.dailyStudyTime}
              onChange={(e) => setFormData({...formData, dailyStudyTime: e.target.value})}
            >
              <option>30 mins</option>
              <option>1 hour</option>
              <option>2 hours</option>
              <option>3+ hours</option>
            </select>
          </div>
        </div>

        <button 
          type="submit" 
          disabled={isLoading}
          className={`w-full py-3 rounded-lg font-semibold text-white transition-all flex items-center justify-center gap-2 ${
            isLoading ? 'bg-[#5427E6]/70 cursor-not-allowed' : 'bg-[#6D4AFF] hover:bg-[#5427E6]'
          }`}
        >
          {isLoading ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              Generating Learning Path...
            </>
          ) : (
            'Generate My Learning Path'
          )}
        </button>
      </div>
    </form>
  );
};

export default CopilotForm;
