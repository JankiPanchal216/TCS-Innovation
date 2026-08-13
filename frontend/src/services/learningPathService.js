import axios from 'axios';

const API_URL = 'http://localhost:8000/api/learning-path';

export const getLearningPath = async (id = 'lp-1') => {
  try {
    const response = await axios.get(`${API_URL}`, { timeout: 3000 });
    return response.data;
  } catch (err) {
    console.warn("LearningPath API fallback activated:", err.message);
    return {
      id: "lp-1",
      title: "Computer Science Foundation",
      progress_percentage: 25,
      time_remaining: "4 Weeks",
      total_resources: 12,
      current_focus: "TCP/IP Fundamentals"
    };
  }
};

export const getLearningPathWeeks = async (id = 'lp-1') => {
  try {
    const response = await axios.get(`${API_URL}/${id}/weeks`, { timeout: 3000 });
    return response.data;
  } catch (err) {
    return [
      {
        week_number: 1,
        status: "CURRENT",
        progress_percentage: 65,
        estimated_remaining_hours: 2.5,
        risk: "Low",
        resources: [
          {
            id: "res-1",
            title: "Computer Networking: A Top-Down Approach",
            author: "Andrew S. Tanenbaum",
            difficulty: "Intermediate",
            estimated_hours: 6,
            match_score: 94,
            progress: 65,
            focus: "Chapters 1-3",
            is_locked: false,
            prerequisites: []
          }
        ]
      },
      {
        week_number: 2,
        status: "UPCOMING",
        progress_percentage: 0,
        estimated_remaining_hours: 8,
        risk: "Low",
        resources: [
          {
            id: "res-2",
            title: "Network Security Essentials",
            author: "William Stallings",
            difficulty: "Advanced",
            estimated_hours: 8,
            match_score: 88,
            progress: 0,
            focus: "Encryption",
            is_locked: true,
            prerequisites: ["TCP/IP Fundamentals"]
          }
        ]
      }
    ];
  }
};

export const getLearningPathAnalytics = async (id = 'lp-1') => {
  try {
    const response = await axios.get(`${API_URL}/${id}/analytics`, { timeout: 3000 });
    return response.data;
  } catch (err) {
    return {
      rationale: "Based on your assessment performance and current progress, TCP/IP Fundamentals has been prioritized before Network Security.",
      pacing: "You are ahead of schedule.",
      next_best_action: "Complete Chapter 3 before starting Network Security Essentials.",
      risk_explanation: null
    };
  }
};

export const regenerateLearningPath = async (id = 'lp-1') => {
  try {
    const response = await axios.post(`${API_URL}/${id}/regenerate`, {}, { timeout: 3000 });
    return response.data;
  } catch (err) {
    return { status: "success", message: "Learning path optimized successfully (offline mode)." };
  }
};
