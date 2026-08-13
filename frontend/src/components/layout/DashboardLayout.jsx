import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import TopHeader from './TopHeader';

const DashboardLayout = () => {
  return (
    <div className="flex min-h-screen bg-[#F7F7FA] font-sans">
      {/* Desktop Sidebar */}
      <div className="hidden md:block w-[260px] flex-shrink-0">
        <Sidebar />
      </div>

      <div className="flex-1 flex flex-col min-w-0">
        <TopHeader />
        <main className="flex-1 p-8 overflow-y-auto">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
