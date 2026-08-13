import React from 'react';
import { topBooks } from '../../data/dashboardData';

const TopBooksTable = () => {
  return (
    <div className="bg-white rounded-xl border border-[#E8E7EF] shadow-sm overflow-hidden">
      <div className="p-6 border-b border-[#E8E7EF] flex justify-between items-center">
        <h3 className="font-bold text-[#17152A] text-lg">Top Books this Month</h3>
        <button className="text-sm font-medium text-[#6D4AFF] hover:text-[#5427E6]">View All</button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#F7F7FA] text-[#747184] text-xs uppercase tracking-wider">
              <th className="px-6 py-4 font-semibold">Title</th>
              <th className="px-6 py-4 font-semibold">Author</th>
              <th className="px-6 py-4 font-semibold">Category</th>
              <th className="px-6 py-4 font-semibold">Borrows</th>
              <th className="px-6 py-4 font-semibold">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#E8E7EF]">
            {topBooks.map((book) => (
              <tr key={book.id} className="hover:bg-[#F7F7FA] transition-colors">
                <td className="px-6 py-4">
                  <div className="font-medium text-[#17152A]">{book.title}</div>
                </td>
                <td className="px-6 py-4 text-sm text-[#747184]">{book.author}</td>
                <td className="px-6 py-4 text-sm text-[#747184]">
                  <span className="px-2.5 py-1 rounded-full bg-[#F7F7FA] border border-[#E8E7EF] text-xs font-medium">
                    {book.category}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-[#17152A] font-medium">{book.borrows}</td>
                <td className="px-6 py-4">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                    book.status === 'Available' ? 'bg-[#16A34A]/10 text-[#16A34A]' : 
                    book.status === 'Low Stock' ? 'bg-[#F59E0B]/10 text-[#F59E0B]' : 
                    'bg-[#BA1A1A]/10 text-[#BA1A1A]'
                  }`}>
                    {book.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TopBooksTable;
