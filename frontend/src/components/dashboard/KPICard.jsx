import React from 'react';

const KPICard = ({ title, value, icon: Icon, trend, trendValue, isAi = false }) => {
  return (
    <div className={`p-5 rounded-xl border ${isAi ? 'border-[#6D4AFF] bg-white' : 'border-[#E8E7EF] bg-white'} shadow-sm`}>
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-[#747184] font-medium text-sm">{title}</h3>
        <div className={`p-2 rounded-lg ${isAi ? 'bg-[#6D4AFF]/10 text-[#6D4AFF]' : 'bg-[#F7F7FA] text-[#747184]'}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <div className="flex items-baseline gap-3">
        <span className="text-3xl font-bold text-[#17152A]">{value}</span>
        {trend && trendValue && (
          <span className={`text-sm font-medium ${trend === 'up' ? 'text-[#16A34A]' : 'text-[#BA1A1A]'}`}>
            {trend === 'up' ? '+' : '-'}{trendValue}
          </span>
        )}
      </div>
    </div>
  );
};

export default KPICard;
