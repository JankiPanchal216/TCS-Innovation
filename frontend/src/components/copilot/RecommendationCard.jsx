import React, { useState } from 'react';
import { Book, CheckCircle, Clock, Copy, ChevronDown, ChevronUp, Plus } from 'lucide-react';
import ExplanationPanel from './ExplanationPanel';

const RecommendationCard = ({ book }) => {
  const [showExplanation, setShowExplanation] = useState(false);
  const [added, setAdded] = useState(false);

  return (
    <div className="bg-white rounded-xl border border-[#E8E7EF] shadow-sm overflow-hidden flex flex-col">
      <div className="p-5 flex-1">
        <div className="flex justify-between items-start mb-3">
          <div className="flex gap-2 items-center">
            <span className="px-2.5 py-1 rounded-full bg-[#6D4AFF]/10 text-[#6D4AFF] text-xs font-bold">
              {book.match_score}% Match
            </span>
            <span className="px-2.5 py-1 rounded-full bg-[#F7F7FA] text-[#747184] text-xs font-medium border border-[#E8E7EF]">
              {book.category}
            </span>
          </div>
          <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
            book.status === 'Available' ? 'bg-[#16A34A]/10 text-[#16A34A]' : 'bg-[#F59E0B]/10 text-[#F59E0B]'
          }`}>
            {book.status}
          </span>
        </div>

        <h4 className="text-lg font-bold text-[#17152A] leading-tight mb-1">{book.title}</h4>
        <p className="text-sm text-[#747184] mb-4">{book.author} • {book.edition}</p>

        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="flex items-center gap-2 text-sm text-[#17152A]">
            <CheckCircle className="w-4 h-4 text-[#747184]" />
            <span className="font-medium">{book.difficulty}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-[#17152A]">
            <Clock className="w-4 h-4 text-[#747184]" />
            <span className="font-medium">Est. {book.estimated_time}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-[#17152A] col-span-2">
            <Copy className="w-4 h-4 text-[#747184]" />
            <span className="font-medium">{book.available_copies} Copies Available</span>
          </div>
        </div>

        {showExplanation && (
          <ExplanationPanel 
            explanation={book.explanation} 
            insight={book.insight}
            matchScore={book.match_score}
          />
        )}
      </div>

      <div className="p-3 bg-[#F7F7FA] border-t border-[#E8E7EF] flex gap-2">
        <button 
          onClick={() => setShowExplanation(!showExplanation)}
          className="flex-1 py-2 rounded-lg bg-white border border-[#E8E7EF] text-sm font-medium text-[#17152A] hover:bg-gray-50 transition-colors flex items-center justify-center gap-1"
        >
          Why this book? {showExplanation ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
        <button 
          onClick={() => setAdded(true)}
          disabled={added}
          className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-1 ${
            added ? 'bg-[#16A34A] text-white' : 'bg-[#6D4AFF] text-white hover:bg-[#5427E6]'
          }`}
        >
          {added ? (
            <>
              <CheckCircle className="w-4 h-4" /> Added to Path
            </>
          ) : (
            <>
              <Plus className="w-4 h-4" /> Add to Path
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default RecommendationCard;
