import React from 'react';
import { Sparkles } from 'lucide-react';

const MetricBar = ({ label, value }) => (
  <div className="flex items-center justify-between gap-4 mb-2">
    <span className="text-sm text-[#747184] w-40">{label}</span>
    <div className="flex-1 h-2 bg-[#F7F7FA] rounded-full overflow-hidden">
      <div 
        className="h-full bg-[#6D4AFF] rounded-full"
        style={{ width: `${value}%` }}
      ></div>
    </div>
    <span className="text-sm font-medium text-[#17152A] w-10 text-right">{value}%</span>
  </div>
);

const ExplanationPanel = ({ explanation, insight, matchScore }) => {
  return (
    <div className="mt-4 p-4 bg-[#F7F7FA] rounded-lg border border-[#E8E7EF]">
      <div className="flex gap-2 items-start mb-4">
        <Sparkles className="w-5 h-5 text-[#6D4AFF] mt-0.5 shrink-0" />
        <p className="text-sm text-[#17152A] leading-relaxed">
          <span className="font-semibold">{matchScore}% Match</span> because {insight.toLowerCase()}
        </p>
      </div>

      <div className="pt-4 border-t border-[#E8E7EF]">
        <h4 className="text-xs font-semibold text-[#17152A] uppercase tracking-wider mb-3">AI Match Breakdown</h4>
        <MetricBar label="Learning Goal Relevance" value={explanation.relevance} />
        <MetricBar label="Skill Coverage" value={explanation.skill_coverage} />
        <MetricBar label="Difficulty Match" value={explanation.difficulty_match} />
        <MetricBar label="Time Fit" value={explanation.time_fit} />
        <MetricBar label="Availability" value={explanation.availability} />
        
        <div className="flex items-center justify-between gap-4 mt-4 pt-3 border-t border-[#E8E7EF]">
          <span className="text-sm font-bold text-[#17152A]">Overall Match</span>
          <span className="text-sm font-bold text-[#6D4AFF]">{matchScore}%</span>
        </div>
      </div>
    </div>
  );
};

export default ExplanationPanel;
