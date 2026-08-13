import React, { useState } from 'react';
import CopilotForm from '../../components/copilot/CopilotForm';
import RecommendationKPI from '../../components/copilot/RecommendationKPI';
import RecommendationCard from '../../components/copilot/RecommendationCard';
import CopilotChat from '../../components/copilot/CopilotChat';
import { generateLearningPath } from '../../services/aiService';

const AICopilot = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [responseTime, setResponseTime] = useState(0);
  const [error, setError] = useState(null);

  const handleGenerate = async (preferences) => {
    setIsLoading(true);
    setError(null);
    const start = performance.now();

    try {
      const data = await generateLearningPath(preferences);
      const end = performance.now();
      setResponseTime(end - start);
      setResults(data);
    } catch (err) {
      setError('Failed to generate learning path. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      <div>
        <h2 className="text-2xl font-bold text-[#17152A]">AI Library Copilot</h2>
        <p className="text-[#747184] text-sm mt-1">Generate a personalized learning path based on your goals and library availability.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <CopilotForm onSubmit={handleGenerate} isLoading={isLoading} />
          
          {error && (
            <div className="p-4 bg-[#BA1A1A]/10 text-[#BA1A1A] rounded-lg border border-[#BA1A1A]/20 font-medium">
              {error}
            </div>
          )}

          {results && !isLoading && (
            <div className="space-y-6 animate-in fade-in duration-500">
              <h3 className="text-lg font-bold text-[#17152A] border-b border-[#E8E7EF] pb-2">Your Recommended Path</h3>
              
              <RecommendationKPI data={results} responseTime={responseTime} />
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {results.recommendations.map(book => (
                  <RecommendationCard key={book.id} book={book} />
                ))}
              </div>
              
              {results.recommendations.length === 0 && (
                <div className="p-8 text-center bg-white rounded-xl border border-[#E8E7EF]">
                  <p className="text-[#747184]">No specific books found matching all criteria, try adjusting your timeline.</p>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="lg:col-span-1">
          <CopilotChat />
        </div>
      </div>
    </div>
  );
};

export default AICopilot;
