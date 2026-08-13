import React, { useState } from 'react';
import { FileText, CheckCircle2, ChevronRight, X } from 'lucide-react';

const ImportHistory = () => {
  const [selectedImport, setSelectedImport] = useState(null);

  const history = [
    { id: 1, file: 'library_inventory.csv', records: 542, source: 'CSV', user: 'Admin', date: 'Aug 13, 2026', status: 'Completed' },
    { id: 2, file: 'library_data.csv', records: 310, source: 'CSV', user: 'Admin', date: 'Aug 12, 2026', status: 'Completed' },
    { id: 3, file: 'unstructured_input', records: 84, source: 'AI Extraction', user: 'Admin', date: 'Aug 12, 2026', status: 'Completed' }
  ];

  return (
    <div className="space-y-6 pb-12">
      <div>
        <h2 className="text-2xl font-bold text-[#17152A]">Import History</h2>
        <p className="text-[#747184] text-sm mt-1">Track previous data ingestion operations.</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-[#E8E7EF] shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-[#E8E7EF] text-xs font-semibold text-[#747184] uppercase">
                <th className="py-3 px-4">File Name</th>
                <th className="py-3 px-4">Records</th>
                <th className="py-3 px-4">Source</th>
                <th className="py-3 px-4">Imported By</th>
                <th className="py-3 px-4">Date</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E8E7EF] text-sm">
              {history.map((h) => (
                <tr key={h.id} className="hover:bg-[#F7F7FA]/50 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-[#17152A] flex items-center gap-2">
                    <FileText className="w-4 h-4 text-[#6D4AFF]" /> {h.file}
                  </td>
                  <td className="py-3.5 px-4 text-[#17152A]">{h.records}</td>
                  <td className="py-3.5 px-4 text-[#747184] text-xs">{h.source}</td>
                  <td className="py-3.5 px-4 text-[#747184] text-xs">{h.user}</td>
                  <td className="py-3.5 px-4 text-[#747184] text-xs">{h.date}</td>
                  <td className="py-3.5 px-4">
                    <span className="px-2.5 py-1 bg-[#16A34A]/10 text-[#16A34A] text-xs font-bold rounded-full">
                      {h.status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button 
                      onClick={() => setSelectedImport(h)}
                      className="px-3 py-1 bg-white border border-[#E8E7EF] rounded text-xs font-medium text-[#17152A] hover:bg-[#F7F7FA]"
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {selectedImport && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white p-6 rounded-xl border border-[#E8E7EF] max-w-lg w-full">
            <div className="flex justify-between items-start mb-4 border-b border-[#E8E7EF] pb-3">
              <div>
                <h3 className="text-lg font-bold text-[#17152A]">Import Summary</h3>
                <p className="text-xs text-[#747184]">{selectedImport.file}</p>
              </div>
              <button onClick={() => setSelectedImport(null)} className="p-1 hover:bg-[#F7F7FA] rounded text-[#747184]"><X className="w-5 h-5" /></button>
            </div>

            <div className="space-y-4 text-sm">
              <div className="grid grid-cols-2 gap-4 bg-[#F7F7FA] p-3 rounded-lg border border-[#E8E7EF]">
                <div><span className="text-[#747184] block text-xs">Imported On</span><span className="font-semibold">{selectedImport.date}</span></div>
                <div><span className="text-[#747184] block text-xs">Records Detected</span><span className="font-semibold">{selectedImport.records}</span></div>
                <div><span className="text-[#747184] block text-xs">Successfully Structured</span><span className="font-semibold text-[#16A34A]">{selectedImport.records - 14}</span></div>
                <div><span className="text-[#747184] block text-xs">Needs Review</span><span className="font-semibold text-[#F59E0B]">14</span></div>
              </div>

              <div>
                <h4 className="text-xs font-semibold text-[#747184] uppercase mb-3">Processing Pipeline</h4>
                <div className="space-y-2">
                  {['File Uploaded', 'Column Detection', 'Data Normalization', 'AI Extraction', 'Validation', 'Database Storage'].map((step, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-xs text-[#17152A]">
                      <CheckCircle2 className="w-4 h-4 text-[#16A34A]" /> {step}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button onClick={() => setSelectedImport(null)} className="px-4 py-2 bg-[#6D4AFF] text-white rounded-lg text-sm font-medium hover:bg-[#5427E6]">Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImportHistory;
