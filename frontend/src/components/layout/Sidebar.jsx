import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Book, 
  BarChart2, 
  Sparkles, 
  Map, 
  FileText, 
  Clock, 
  AlertTriangle, 
  PieChart, 
  Settings, 
  HelpCircle, 
  User,
  Database,
  Layers,
  History,
  Shield,
  LogOut,
  X
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const Sidebar = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  const mainNavItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Books', path: '/books', icon: Book },
    { name: 'Analytics', path: '/analytics', icon: BarChart2 },
    { name: 'AI Copilot', path: '/student/copilot', icon: Sparkles },
    { name: 'Learning Path', path: '/learning-path', icon: Map },
    { name: 'Syllabus Intelligence', path: '/syllabus', icon: FileText },
    { name: 'Overdue & Deadlines', path: '/overdue', icon: Clock },
    { name: 'Reader Risk', path: '/reader-risk', icon: AlertTriangle },
    { name: 'Reports', path: '/reports', icon: PieChart },
  ];

  const adminNavItems = [
    { name: 'Data Management', path: '/admin/data-management', icon: Database },
    { name: 'Book Inventory', path: '/admin/book-inventory', icon: Layers },
    { name: 'Import History', path: '/admin/import-history', icon: History },
    { name: 'Admin Settings', path: '/admin/settings', icon: Shield },
  ];

  const handleLogout = () => {
    logout();
    setShowLogoutModal(false);
    navigate('/login');
  };

  return (
    <aside className="w-64 bg-[#17152A] text-white flex flex-col h-screen fixed left-0 top-0 border-r border-[#3E3A5A] z-30">
      {/* Brand Header */}
      <div className="p-5 border-b border-white/10 flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-[#6D4AFF] flex items-center justify-center font-bold text-lg text-white shadow-md">
          L
        </div>
        <div>
          <h1 className="font-bold text-base tracking-tight leading-none text-white">LibraAI</h1>
          <span className="text-[11px] text-white/50 font-medium">Intelligent Library OS</span>
        </div>
      </div>

      {/* Main Navigation */}
      <div className="flex-1 overflow-y-auto py-4 px-3 space-y-6">
        <nav className="space-y-1">
          {mainNavItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.name}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-[#6D4AFF] text-white shadow-sm'
                      : 'text-white/70 hover:bg-white/5 hover:text-white'
                  }`
                }
              >
                <Icon className="w-4 h-4" />
                {item.name}
              </NavLink>
            );
          })}
        </nav>

        <div className="border-t border-white/10 pt-4">
          <p className="px-3 text-[10px] font-semibold text-white/40 uppercase tracking-wider mb-2">Administration</p>
          <nav className="space-y-1">
            {adminNavItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.name}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-[#6D4AFF] text-white shadow-sm'
                        : 'text-white/70 hover:bg-white/5 hover:text-white'
                    }`
                  }
                >
                  <Icon className="w-4 h-4" />
                  {item.name}
                </NavLink>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Sidebar Footer */}
      <div className="p-3 border-t border-white/10 space-y-1">
        <button 
          onClick={() => setShowLogoutModal(true)}
          className="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm font-medium text-[#BA1A1A] hover:bg-[#BA1A1A]/10 transition-all"
        >
          <LogOut className="w-4 h-4" />
          Logout
        </button>
      </div>

      {showLogoutModal && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
          <div className="bg-white text-[#17152A] p-6 rounded-xl border border-[#E8E7EF] max-w-sm w-full shadow-2xl">
            <h3 className="text-lg font-bold mb-2">Sign out of LibraAI?</h3>
            <p className="text-sm text-[#747184] mb-6">You will need to sign in again to access the administration console.</p>
            <div className="flex justify-end gap-2">
              <button onClick={() => setShowLogoutModal(false)} className="px-4 py-2 border border-[#E8E7EF] rounded-lg text-sm font-medium text-[#747184] hover:bg-[#F7F7FA]">Cancel</button>
              <button onClick={handleLogout} className="px-4 py-2 bg-[#BA1A1A] text-white rounded-lg text-sm font-medium hover:bg-red-700">Sign Out</button>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
};

export default Sidebar;
