import React from 'react';
import { Sparkles, ChevronRight, Lightbulb } from 'lucide-react';
import { aiInsights } from '../../data/dashboardData';
import { useNavigate } from 'react-router-dom';

const AIInsightsCard = () => {
  const navigate = useNavigate();

  return (
    <div className="bg-gradient-to-br from-[#17152A] to-[#2A2645] rounded-xl shadow-lg border border-[#3E3A5A] text-white p-6 h-full flex flex-col">
      <div className="flex items-center gap-2 mb-6">
        <Sparkles className="w-6 h-6 text-[#6D4AFF]" />
        <h3 className="font-bold text-lg">AI Library Insights</h3>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto">
        {aiInsights.map((insight) => (
          <div key={insight.id} className="bg-white/10 p-4 rounded-lg border border-white/10 hover:bg-white/15 transition-colors">
            <div className="flex items-start gap-3">
              <div className="mt-0.5">
                <Lightbulb className="w-5 h-5 text-[#6D4AFF]" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-sm mb-1">{insight.title}</h4>
                <p className="text-xs text-white/80 mb-3 leading-relaxed">{insight.insight}</p>
                <button 
                  className="text-xs font-medium text-[#6D4AFF] flex items-center gap-1 hover:text-white transition-colors"
                  onClick={() => navigate('/ai-recommendations')}
                >
                  {insight.action} <ChevronRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AIInsightsCard;
