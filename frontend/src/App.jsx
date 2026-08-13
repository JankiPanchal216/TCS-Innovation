import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import DashboardLayout from './components/layout/DashboardLayout';
import LibraryDashboard from './pages/LibraryDashboard';
import AICopilot from './pages/student/AICopilot';
import MyLearningPath from './pages/student/MyLearningPath';
import Login from './pages/auth/Login';
import DataManagement from './pages/admin/DataManagement';
import BookInventory from './pages/admin/BookInventory';
import ImportHistory from './pages/admin/ImportHistory';
import AdminSettings from './pages/admin/AdminSettings';

// Placeholder components for other routes
const Placeholder = ({ title }) => (
  <div className="flex items-center justify-center h-64 bg-white rounded-xl border border-[#E8E7EF]">
    <h2 className="text-xl font-medium text-[#747184]">{title} Page (Under Construction)</h2>
  </div>
);

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          
          <Route element={<DashboardLayout />}>
            <Route path="/dashboard" element={<LibraryDashboard />} />
            <Route path="/books" element={<Placeholder title="Books" />} />
            <Route path="/analytics" element={<Placeholder title="Analytics" />} />
            <Route path="/student/copilot" element={<AICopilot />} />
            <Route path="/ai-recommendations" element={<Navigate to="/student/copilot" replace />} />
            <Route path="/learning-path" element={<MyLearningPath />} />
            <Route path="/syllabus" element={<Placeholder title="Syllabus Intelligence" />} />
            <Route path="/overdue" element={<Placeholder title="Overdue & Deadlines" />} />
            <Route path="/reader-risk" element={<Placeholder title="Reader Risk" />} />
            <Route path="/reports" element={<Placeholder title="Reports" />} />
            
            {/* Admin Routes */}
            <Route path="/admin/data-management" element={<DataManagement />} />
            <Route path="/admin/book-inventory" element={<BookInventory />} />
            <Route path="/admin/import-history" element={<ImportHistory />} />
            <Route path="/admin/settings" element={<AdminSettings />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
