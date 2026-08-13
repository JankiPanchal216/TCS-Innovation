import React, { useEffect, useState } from 'react';
import { Target, Clock, BookOpen, Map, RefreshCw, AlertTriangle, CheckCircle, ChevronRight, PlayCircle } from 'lucide-react';
import { getLearningPath, getLearningPathWeeks, getLearningPathAnalytics, regenerateLearningPath } from '../../services/learningPathService';

const MyLearningPath = () => {
  const [path, setPath] = useState(null);
  const [weeks, setWeeks] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [pathData, weeksData, analyticsData] = await Promise.all([
        getLearningPath(),
        getLearningPathWeeks(),
        getLearningPathAnalytics()
      ]);
      setPath(pathData);
      setWeeks(weeksData);
      setAnalytics(analyticsData);
    } catch (error) {
      console.error("Error loading learning path:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerate = async () => {
    setRegenerating(true);
    try {
      await regenerateLearningPath();
      await fetchData();
    } catch (error) {
      console.error("Error regenerating path:", error);
    } finally {
      setRegenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96">
        <div className="w-8 h-8 border-4 border-[#6D4AFF] border-t-transparent rounded-full animate-spin"></div>
        <p className="mt-4 text-[#747184]">Loading learning path...</p>
      </div>
    );
  }

  if (!path) {
    return (
      <div className="flex flex-col items-center justify-center h-96 bg-white rounded-xl border border-[#E8E7EF]">
        <Map className="w-12 h-12 text-[#747184] mb-4" />
        <h2 className="text-xl font-bold text-[#17152A]">No Learning Path Found</h2>
        <p className="text-[#747184] mb-4">You don't have a learning path yet.</p>
        <button className="px-6 py-2 bg-[#6D4AFF] text-white rounded-lg font-medium hover:bg-[#5427E6]">
          Create Learning Path
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-12">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-[#17152A]">My Learning Path</h2>
          <p className="text-[#747184] text-sm mt-1">{path.title}</p>
        </div>
        <button 
          onClick={handleRegenerate}
          disabled={regenerating}
          className="flex items-center gap-2 px-4 py-2 bg-white border border-[#E8E7EF] rounded-lg text-sm font-medium text-[#17152A] hover:bg-[#F7F7FA] disabled:opacity-50 transition-colors"
        >
          <RefreshCw className={`w-4 h-4 ${regenerating ? 'animate-spin text-[#6D4AFF]' : ''}`} />
          {regenerating ? 'Regenerating...' : 'Regenerate Path'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-[#E8E7EF] shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-[#747184] font-medium text-sm">Overall Progress</h3>
            <div className="p-2 rounded-lg bg-[#F7F7FA] text-[#747184]"><Target className="w-5 h-5" /></div>
          </div>
          <div className="flex items-baseline gap-2 mb-2">
            <span className="text-3xl font-bold text-[#17152A]">{path.progress_percentage}%</span>
          </div>
          <div className="w-full bg-[#F7F7FA] rounded-full h-1.5 overflow-hidden">
            <div className="bg-[#6D4AFF] h-1.5 rounded-full" style={{ width: `${path.progress_percentage}%` }}></div>
          </div>
        </div>
        
        <div className="bg-white p-5 rounded-xl border border-[#E8E7EF] shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-[#747184] font-medium text-sm">Time Remaining</h3>
            <div className="p-2 rounded-lg bg-[#F7F7FA] text-[#747184]"><Clock className="w-5 h-5" /></div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-[#17152A]">{path.time_remaining}</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-[#E8E7EF] shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-[#747184] font-medium text-sm">Resources</h3>
            <div className="p-2 rounded-lg bg-[#F7F7FA] text-[#747184]"><BookOpen className="w-5 h-5" /></div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-[#17152A]">{path.total_resources}</span>
            <span className="text-sm font-medium text-[#747184]">Books</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-[#E8E7EF] shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-[#747184] font-medium text-sm">Current Focus</h3>
            <div className="p-2 rounded-lg bg-[#F7F7FA] text-[#747184]"><Map className="w-5 h-5" /></div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-lg font-bold text-[#17152A] leading-tight">{path.current_focus}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {weeks.map((week) => (
            <div key={week.week_number} className={`bg-white rounded-xl border ${week.status === 'CURRENT' ? 'border-[#6D4AFF] shadow-md' : 'border-[#E8E7EF]'} overflow-hidden`}>
              <div className={`p-4 border-b ${week.status === 'CURRENT' ? 'border-[#6D4AFF]/20 bg-[#6D4AFF]/5' : 'border-[#E8E7EF] bg-[#F7F7FA]'} flex justify-between items-center`}>
                <h3 className="font-bold text-[#17152A]">Week {week.week_number}</h3>
                <div className="flex items-center gap-4 text-sm font-medium">
                  {week.status === 'CURRENT' && (
                    <span className="text-[#6D4AFF]">{week.progress_percentage}% Complete</span>
                  )}
                  {week.status === 'CURRENT' && (
                    <span className="text-[#747184]">{week.estimated_remaining_hours}h Remaining</span>
                  )}
                  <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                    week.status === 'CURRENT' ? 'bg-[#6D4AFF]/10 text-[#6D4AFF]' :
                    week.status === 'UPCOMING' ? 'bg-[#F7F7FA] text-[#747184] border border-[#E8E7EF]' :
                    'bg-[#16A34A]/10 text-[#16A34A]'
                  }`}>
                    {week.status}
                  </span>
                </div>
              </div>
              <div className="p-5">
                {week.resources.map(res => (
                  <div key={res.id} className={`flex flex-col md:flex-row gap-4 ${res.is_locked ? 'opacity-60' : ''}`}>
                    <div className="flex-1">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-bold text-[#17152A] text-lg">{res.title}</h4>
                        <span className="px-2 py-1 bg-[#6D4AFF]/10 text-[#6D4AFF] text-xs font-bold rounded-full">
                          {res.match_score}% Match
                        </span>
                      </div>
                      <p className="text-sm text-[#747184] mb-3">{res.author}</p>
                      
                      <div className="flex flex-wrap items-center gap-4 text-sm text-[#747184] mb-4">
                        <div className="flex items-center gap-1.5">
                          <CheckCircle className="w-4 h-4" /> {res.difficulty}
                        </div>
                        <div className="flex items-center gap-1.5">
                          <Clock className="w-4 h-4" /> {res.estimated_hours} Hours
                        </div>
                      </div>

                      <div className="bg-[#F7F7FA] p-3 rounded-lg border border-[#E8E7EF]">
                        <p className="text-sm font-medium text-[#17152A] mb-1">Focus:</p>
                        <p className="text-sm text-[#747184]">{res.focus}</p>
                      </div>

                      {res.is_locked && res.prerequisites.length > 0 && (
                        <div className="mt-3 flex items-center gap-2 text-sm text-[#F59E0B] font-medium bg-[#F59E0B]/10 p-2 rounded-lg">
                          <AlertTriangle className="w-4 h-4" />
                          Prerequisite required: {res.prerequisites.join(', ')}
                        </div>
                      )}
                    </div>

                    <div className="flex flex-col justify-end gap-2 md:min-w-[160px]">
                      <button disabled={res.is_locked} className="flex items-center justify-center gap-2 w-full py-2 bg-[#6D4AFF] text-white rounded-lg text-sm font-medium hover:bg-[#5427E6] disabled:opacity-50 transition-colors">
                        <PlayCircle className="w-4 h-4" /> Continue
                      </button>
                      <button className="w-full py-2 bg-white border border-[#E8E7EF] text-[#17152A] rounded-lg text-sm font-medium hover:bg-[#F7F7FA] transition-colors">
                        View Book
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="lg:col-span-1">
          <div className="bg-gradient-to-br from-[#17152A] to-[#2A2645] rounded-xl shadow-lg border border-[#3E3A5A] text-white p-6 h-full flex flex-col sticky top-24">
            <h3 className="font-bold text-lg flex items-center gap-2 mb-6">
              AI Learning Strategy
            </h3>

            {analytics && (
              <div className="space-y-6">
                <div>
                  <h4 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-2">The Rationale</h4>
                  <p className="text-sm text-white/90 leading-relaxed bg-white/5 p-3 rounded-lg border border-white/10">
                    {analytics.rationale}
                  </p>
                </div>

                <div>
                  <h4 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-2">Pacing Recommendation</h4>
                  <div className="flex items-center gap-2 text-sm text-[#16A34A] font-medium bg-[#16A34A]/10 p-3 rounded-lg border border-[#16A34A]/20">
                    <CheckCircle className="w-4 h-4" /> {analytics.pacing}
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-2">Next Best Action</h4>
                  <button className="w-full text-left p-3 bg-[#6D4AFF] hover:bg-[#5427E6] rounded-lg transition-colors flex justify-between items-center group">
                    <span className="text-sm font-medium">{analytics.next_best_action}</span>
                    <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>

                {analytics.risk_explanation && (
                  <div>
                    <h4 className="text-xs font-semibold text-[#BA1A1A] uppercase tracking-wider mb-2">Risk Alert</h4>
                    <p className="text-sm text-[#BA1A1A] leading-relaxed bg-[#BA1A1A]/10 p-3 rounded-lg border border-[#BA1A1A]/20">
                      {analytics.risk_explanation}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MyLearningPath;
