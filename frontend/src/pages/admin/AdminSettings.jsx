import React, { useState } from 'react';
import { Shield, Key, Sliders } from 'lucide-react';

const AdminSettings = () => {
  const [threshold, setThreshold] = useState(85);

  return (
    <div className="space-y-6 pb-12">
      <div>
        <h2 className="text-2xl font-bold text-[#17152A]">Admin Settings</h2>
        <p className="text-[#747184] text-sm mt-1">Configure security, profiles, and data processing rules.</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-[#E8E7EF] shadow-sm space-y-6 max-w-2xl">
        <div>
          <h3 className="text-lg font-bold text-[#17152A] mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-[#6D4AFF]" /> Administrator Profile
          </h3>
          <div className="grid grid-cols-1 gap-4">
            <div>
              <label className="block text-sm font-medium text-[#747184] mb-1">Name</label>
              <input type="text" defaultValue="System Admin" className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg px-3 py-2 text-sm text-[#17152A]" />
            </div>
            <div>
              <label className="block text-sm font-medium text-[#747184] mb-1">Email</label>
              <input type="email" defaultValue="admin@libraai.com" className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg px-3 py-2 text-sm text-[#17152A]" />
            </div>
          </div>
        </div>

        <div className="border-t border-[#E8E7EF] pt-6">
          <h3 className="text-lg font-bold text-[#17152A] mb-4 flex items-center gap-2">
            <Sliders className="w-5 h-5 text-[#6D4AFF]" /> Data Processing Settings
          </h3>
          <div>
            <label className="block text-sm font-medium text-[#17152A] mb-1">AI Confidence Threshold ({threshold}%)</label>
            <input 
              type="range" 
              min="50" 
              max="99" 
              value={threshold}
              onChange={(e) => setThreshold(e.target.value)}
              className="w-full text-[#6D4AFF]" 
            />
            <p className="text-xs text-[#747184] mt-1">Records below this confidence score will require manual administrator review.</p>
          </div>
        </div>

        <div className="flex justify-end pt-4 border-t border-[#E8E7EF]">
          <button className="px-5 py-2 bg-[#6D4AFF] text-white rounded-lg text-sm font-medium hover:bg-[#5427E6]">
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdminSettings;
