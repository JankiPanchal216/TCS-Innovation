import React from 'react';
import KPICard from '../components/dashboard/KPICard';
import BorrowingActivityChart from '../components/dashboard/BorrowingActivityChart';
import AIInsightsCard from '../components/dashboard/AIInsightsCard';
import TopBooksTable from '../components/dashboard/TopBooksTable';
import { KPIs } from '../data/dashboardData';
import { Book, Users, BookOpen, AlertTriangle, Sparkles } from 'lucide-react';

const LibraryDashboard = () => {
  return (
    <div className="space-y-6 pb-12">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-[#17152A]">Library Intelligence</h2>
          <p className="text-[#747184] text-sm mt-1">Overview of today's library performance and AI insights.</p>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <KPICard 
          title="Total Books" 
          value={KPIs.totalBooks.toLocaleString()} 
          icon={Book} 
        />
        <KPICard 
          title="Active Readers" 
          value={KPIs.activeReaders.toLocaleString()} 
          icon={Users} 
          trend="up" 
          trendValue="12%" 
        />
        <KPICard 
          title="Books Issued" 
          value={KPIs.booksIssued.toLocaleString()} 
          icon={BookOpen} 
          trend="up" 
          trendValue="5%" 
        />
        <KPICard 
          title="Overdue Books" 
          value={KPIs.overdueBooks.toLocaleString()} 
          icon={AlertTriangle} 
          trend="down" 
          trendValue="2%" 
        />
        <KPICard 
          title="AI Match Score" 
          value={`${KPIs.aiMatch}%`} 
          icon={Sparkles} 
          isAi={true} 
        />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <BorrowingActivityChart />
        </div>
        <div className="lg:col-span-1">
          <AIInsightsCard />
        </div>
      </div>

      {/* Tables Section */}
      <div className="grid grid-cols-1 gap-6">
        <TopBooksTable />
      </div>

    </div>
  );
};

export default LibraryDashboard;
