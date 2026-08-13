import React from 'react';
import { Target, CheckCircle2, Clock, Zap } from 'lucide-react';

const RecommendationKPI = ({ data, responseTime }) => {
  if (!data) return null;

  return (
    <div className="bg-white p-4 rounded-xl border border-[#E8E7EF] shadow-sm flex flex-wrap gap-6 items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-[#6D4AFF]/10 flex items-center justify-center text-[#6D4AFF]">
          <Zap className="w-5 h-5" />
        </div>
        <div>
          <p className="text-xs text-[#747184] font-medium">AI Match Score</p>
          <p className="text-lg font-bold text-[#17152A]">{data.match_score}%</p>
        </div>
      </div>

      <div className="h-8 w-px bg-[#E8E7EF] hidden md:block"></div>

      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-[#16A34A]/10 flex items-center justify-center text-[#16A34A]">
          <Target className="w-5 h-5" />
        </div>
        <div>
          <p className="text-xs text-[#747184] font-medium">Goal Coverage</p>
          <p className="text-lg font-bold text-[#17152A]">{data.goal_coverage}%</p>
        </div>
      </div>

      <div className="h-8 w-px bg-[#E8E7EF] hidden md:block"></div>

      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-[#F7F7FA] flex items-center justify-center text-[#747184]">
          <CheckCircle2 className="w-5 h-5" />
        </div>
        <div>
          <p className="text-xs text-[#747184] font-medium">Resources Available</p>
          <p className="text-lg font-bold text-[#17152A]">{data.resources_available}/{data.total_resources}</p>
        </div>
      </div>

      <div className="h-8 w-px bg-[#E8E7EF] hidden md:block"></div>

      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-[#F7F7FA] flex items-center justify-center text-[#747184]">
          <Clock className="w-5 h-5" />
        </div>
        <div>
          <p className="text-xs text-[#747184] font-medium">Est. Completion</p>
          <p className="text-lg font-bold text-[#17152A]">{data.estimated_completion_days} Days</p>
        </div>
      </div>

      <div className="h-8 w-px bg-[#E8E7EF] hidden lg:block"></div>

      <div className="flex flex-col items-end">
        <p className="text-xs text-[#747184] font-medium">AI Response Time</p>
        <div className="flex items-center gap-1.5 mt-0.5">
          <p className="text-sm font-bold text-[#17152A]">{(responseTime / 1000).toFixed(1)}s</p>
          {responseTime < 10000 ? (
            <span className="text-[10px] font-medium text-[#16A34A] bg-[#16A34A]/10 px-2 py-0.5 rounded-full">✓ Within target</span>
          ) : (
            <span className="text-[10px] font-medium text-[#BA1A1A] bg-[#BA1A1A]/10 px-2 py-0.5 rounded-full">⚠ Above target</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecommendationKPI;
