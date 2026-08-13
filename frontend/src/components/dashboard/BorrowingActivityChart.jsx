import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { borrowingActivity } from '../../data/dashboardData';

const BorrowingActivityChart = () => {
  const [filter, setFilter] = useState('7D');
  const filters = ['7D', '30D', '3M', '1Y'];

  return (
    <div className="bg-white p-6 rounded-xl border border-[#E8E7EF] shadow-sm flex flex-col h-full">
      <div className="flex justify-between items-center mb-6">
        <h3 className="font-bold text-[#17152A] text-lg">Borrowing Activity</h3>
        <div className="flex gap-2">
          {filters.map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                filter === f 
                  ? 'bg-[#17152A] text-white' 
                  : 'bg-[#F7F7FA] text-[#747184] hover:bg-[#E8E7EF]'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>
      
      <div className="flex-1 w-full min-h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={borrowingActivity} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorIssued" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6D4AFF" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#6D4AFF" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E8E7EF" />
            <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#747184', fontSize: 12 }} dy={10} />
            <YAxis axisLine={false} tickLine={false} tick={{ fill: '#747184', fontSize: 12 }} />
            <Tooltip 
              contentStyle={{ borderRadius: '8px', border: '1px solid #E8E7EF', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Area type="monotone" dataKey="issued" stroke="#6D4AFF" strokeWidth={2} fillOpacity={1} fill="url(#colorIssued)" />
            <Area type="monotone" dataKey="returned" stroke="#16A34A" strokeWidth={2} fillOpacity={0} />
            <Area type="monotone" dataKey="overdue" stroke="#BA1A1A" strokeWidth={2} fillOpacity={0} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default BorrowingActivityChart;
