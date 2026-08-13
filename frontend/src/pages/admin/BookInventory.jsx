import React, { useState } from 'react';
import { Search, Filter, Trash2, Edit2, Eye, AlertTriangle } from 'lucide-react';

const BookInventory = () => {
  const [search, setSearch] = useState('');
  const [deleteId, setDeleteId] = useState(null);

  const [books, setBooks] = useState([
    { id: 1, name: 'Computer Networks', category: 'Computer Science', availability: 'Available', source: 'CSV Import', updated: 'Today' },
    { id: 2, name: 'Operating Systems Concepts', category: 'Computer Science', availability: 'Borrowed', source: 'AI Structuring', updated: 'Today' },
    { id: 3, name: 'Introduction to Algorithms', category: 'Mathematics', availability: 'Available', source: 'Manual Entry', updated: 'Yesterday' },
    { id: 4, name: 'Design Patterns', category: 'Software Engineering', availability: 'Available', source: 'CSV Import', updated: 'Aug 10, 2026' }
  ]);

  const handleDelete = () => {
    setBooks(books.filter(b => b.id !== deleteId));
    setDeleteId(null);
  };

  return (
    <div className="space-y-6 pb-12">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-[#17152A]">Book Inventory</h2>
          <p className="text-[#747184] text-sm mt-1">Manage structured library records.</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-[#E8E7EF] shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row gap-4 justify-between items-center">
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 text-[#747184] absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search books..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg pl-9 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#6D4AFF]"
            />
          </div>

          <div className="flex gap-2 w-full md:w-auto">
            <select className="bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg px-3 py-2 text-sm text-[#17152A]">
              <option>All Categories</option>
              <option>Computer Science</option>
              <option>Mathematics</option>
              <option>Software Engineering</option>
            </select>
            <select className="bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg px-3 py-2 text-sm text-[#17152A]">
              <option>All Sources</option>
              <option>CSV Import</option>
              <option>AI Structuring</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-[#E8E7EF] text-xs font-semibold text-[#747184] uppercase">
                <th className="py-3 px-4">Book Name</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Availability</th>
                <th className="py-3 px-4">Source</th>
                <th className="py-3 px-4">Last Updated</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E8E7EF] text-sm">
              {books
                .filter(b => b.name.toLowerCase().includes(search.toLowerCase()))
                .map((b) => (
                  <tr key={b.id} className="hover:bg-[#F7F7FA]/50 transition-colors">
                    <td className="py-3.5 px-4 font-bold text-[#17152A]">{b.name}</td>
                    <td className="py-3.5 px-4 text-[#747184]">{b.category}</td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                        b.availability === 'Available' ? 'bg-[#16A34A]/10 text-[#16A34A]' : 'bg-[#F59E0B]/10 text-[#F59E0B]'
                      }`}>
                        {b.availability}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-[#747184] text-xs">{b.source}</td>
                    <td className="py-3.5 px-4 text-[#747184] text-xs">{b.updated}</td>
                    <td className="py-3.5 px-4 text-right">
                      <div className="flex justify-end gap-2">
                        <button className="p-1.5 hover:bg-[#E8E7EF] rounded text-[#747184]"><Eye className="w-4 h-4" /></button>
                        <button className="p-1.5 hover:bg-[#E8E7EF] rounded text-[#747184]"><Edit2 className="w-4 h-4" /></button>
                        <button onClick={() => setDeleteId(b.id)} className="p-1.5 hover:bg-[#BA1A1A]/10 rounded text-[#BA1A1A]"><Trash2 className="w-4 h-4" /></button>
                      </div>
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>

      {deleteId && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white p-6 rounded-xl border border-[#E8E7EF] max-w-md w-full">
            <div className="flex items-center gap-3 text-[#BA1A1A] mb-3">
              <AlertTriangle className="w-6 h-6" />
              <h3 className="text-lg font-bold text-[#17152A]">Delete Record</h3>
            </div>
            <p className="text-sm text-[#747184] mb-6">Are you sure you want to delete this book record? This action cannot be undone.</p>
            <div className="flex justify-end gap-2">
              <button onClick={() => setDeleteId(null)} className="px-4 py-2 border border-[#E8E7EF] rounded-lg text-sm text-[#747184] hover:bg-[#F7F7FA]">Cancel</button>
              <button onClick={handleDelete} className="px-4 py-2 bg-[#BA1A1A] text-white rounded-lg text-sm font-medium hover:bg-red-700">Delete</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BookInventory;
