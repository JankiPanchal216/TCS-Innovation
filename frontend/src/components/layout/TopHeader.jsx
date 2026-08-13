import React, { useState } from 'react';
import { Search, Bell, HelpCircle } from 'lucide-react';

const TopHeader = () => {
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <header className="h-[64px] bg-white border-b border-[#E8E7EF] flex items-center justify-between px-8 sticky top-0 z-10">
      <div className="flex-1 max-w-xl">
        <div className="relative">
          <Search className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-[#747184]" />
          <input
            type="text"
            placeholder="Search books, readers, insights..."
            className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#6D4AFF] focus:border-transparent transition-all"
          />
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-[#F7F7FA] rounded-full border border-[#E8E7EF]">
          <span className="w-2 h-2 rounded-full bg-[#16A34A]"></span>
          <span className="text-xs font-medium text-[#747184]">TCS CHARUSAT</span>
        </div>

        <div className="flex items-center gap-4">
          <button className="text-[#747184] hover:text-[#17152A] transition-colors">
            <HelpCircle className="w-5 h-5" />
          </button>
          
          <div className="relative">
            <button 
              className="text-[#747184] hover:text-[#17152A] transition-colors relative"
              onClick={() => setShowNotifications(!showNotifications)}
            >
              <Bell className="w-5 h-5" />
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-[#BA1A1A] rounded-full border-2 border-white"></span>
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-[#E8E7EF] py-2">
                <div className="px-4 py-2 border-b border-[#E8E7EF]">
                  <h3 className="font-semibold text-[#17152A]">Notifications</h3>
                </div>
                <div className="max-h-64 overflow-y-auto">
                  <div className="px-4 py-3 hover:bg-[#F7F7FA] cursor-pointer border-b border-[#E8E7EF] last:border-0">
                    <p className="text-sm font-medium text-[#17152A]">12 books overdue</p>
                    <p className="text-xs text-[#747184] mt-1">Review overdue list for follow-up.</p>
                  </div>
                  <div className="px-4 py-3 hover:bg-[#F7F7FA] cursor-pointer border-b border-[#E8E7EF] last:border-0">
                    <p className="text-sm font-medium text-[#17152A]">High demand for Cybersecurity</p>
                    <p className="text-xs text-[#747184] mt-1">Consider adding new inventory.</p>
                  </div>
                  <div className="px-4 py-3 hover:bg-[#F7F7FA] cursor-pointer border-b border-[#E8E7EF] last:border-0">
                    <p className="text-sm font-medium text-[#17152A]">3 readers at high risk</p>
                    <p className="text-xs text-[#747184] mt-1">Send automated reminders.</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="h-8 w-8 rounded-full bg-[#6D4AFF] text-white flex items-center justify-center font-semibold text-sm border-2 border-white shadow-sm cursor-pointer">
            AD
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopHeader;
