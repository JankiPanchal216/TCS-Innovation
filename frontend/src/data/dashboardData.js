export const KPIs = {
  totalBooks: 45210,
  activeReaders: 12450,
  booksIssued: 8432,
  overdueBooks: 412,
  aiMatch: 94
};

export const borrowingActivity = [
  { name: 'Mon', issued: 400, returned: 240, overdue: 20 },
  { name: 'Tue', issued: 300, returned: 139, overdue: 15 },
  { name: 'Wed', issued: 200, returned: 980, overdue: 30 },
  { name: 'Thu', issued: 278, returned: 390, overdue: 25 },
  { name: 'Fri', issued: 189, returned: 480, overdue: 10 },
  { name: 'Sat', issued: 239, returned: 380, overdue: 5 },
  { name: 'Sun', issued: 349, returned: 430, overdue: 12 },
];

export const popularCategories = [
  { category: 'Computer Science', percentage: 35 },
  { category: 'Business & Management', percentage: 25 },
  { category: 'Engineering', percentage: 20 },
  { category: 'Mathematics', percentage: 15 },
  { category: 'Literature', percentage: 5 },
];

export const libraryHealth = {
  bookUtilization: 78,
  onTimeReturn: 92,
  avgDuration: '14 Days',
  searchTime: '1.2s'
};

export const topBooks = [
  { id: 1, title: 'Clean Code', author: 'Robert C. Martin', category: 'Computer Science', borrows: 450, status: 'Available' },
  { id: 2, title: 'Design Patterns', author: 'Erich Gamma', category: 'Computer Science', borrows: 320, status: 'Low Stock' },
  { id: 3, title: 'The Lean Startup', author: 'Eric Ries', category: 'Business', borrows: 280, status: 'Available' },
  { id: 4, title: 'Introduction to Algorithms', author: 'Thomas H. Cormen', category: 'Computer Science', borrows: 210, status: 'Unavailable' },
  { id: 5, title: 'Principles of Physics', author: 'David Halliday', category: 'Physics', borrows: 190, status: 'Available' },
];

export const aiInsights = [
  {
    id: 1,
    title: 'High Demand Prediction',
    insight: 'Machine Learning textbooks will see a 40% spike in demand next week due to midterms.',
    action: 'Review Inventory'
  },
  {
    id: 2,
    title: 'Reader Risk Alert',
    insight: '12 students have overdue books longer than 30 days. Recommend automated follow-up.',
    action: 'Send Reminders'
  },
  {
    id: 3,
    title: 'Syllabus Alignment',
    insight: 'New Data Science curriculum requires 5 updated titles. Budget allocation suggested.',
    action: 'View Recommendations'
  }
];
