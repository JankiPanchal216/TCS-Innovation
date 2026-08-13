export const generateLearningPath = async (preferences) => {
  // Simulate network delay between 2 to 4 seconds
  const delay = Math.floor(Math.random() * 2000) + 2000;
  
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        match_score: 94,
        goal_coverage: 91,
        resources_available: 6,
        total_resources: 8,
        estimated_completion_days: 14,
        recommendations: [
          {
            id: 'rec-1',
            title: 'Computer Networking: A Top-Down Approach',
            author: 'James Kurose, Keith Ross',
            edition: '8th Edition',
            category: 'Computer Science',
            match_score: 94,
            difficulty: 'Intermediate',
            estimated_time: '14 Days',
            available_copies: 4,
            status: 'Available',
            insight: 'This book covers network fundamentals, TCP/IP, routing, and security prerequisites required for your learning goal.',
            explanation: {
              relevance: 95,
              skill_coverage: 92,
              difficulty_match: 90,
              time_fit: 88,
              availability: 100,
            }
          },
          {
            id: 'rec-2',
            title: 'Cryptography and Network Security',
            author: 'William Stallings',
            edition: '7th Edition',
            category: 'Cybersecurity',
            match_score: 88,
            difficulty: 'Advanced',
            estimated_time: '21 Days',
            available_copies: 2,
            status: 'Low Stock',
            insight: 'Provides the required deep dive into encryption algorithms necessary for modern network architecture.',
            explanation: {
              relevance: 85,
              skill_coverage: 95,
              difficulty_match: 80,
              time_fit: 80,
              availability: 100,
            }
          }
        ]
      });
    }, delay);
  });
};

export const askCopilot = async (question) => {
  const delay = Math.floor(Math.random() * 1000) + 500;
  
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        answer: `This is a simulated AI response to: "${question}". In a real scenario, this would stream from the backend LLM.`
      });
    }, delay);
  });
};
