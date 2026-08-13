import React, { useState } from 'react';
import { Upload, Sparkles, CheckCircle2, AlertTriangle, FileText, Check, X, ShieldAlert } from 'lucide-react';

const DataManagement = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const [unstructuredText, setUnstructuredText] = useState('');
  const [structuring, setStructuring] = useState(false);

  const [records, setRecords] = useState([]);
  const [showValidation, setShowValidation] = useState(false);
  const [notification, setNotification] = useState(null);

  const handleFileUpload = (e) => {
    const uploadedFile = e.target.files?.[0] || { name: 'library_inventory.csv', size: '2.4 MB' };
    setFile(uploadedFile);
    setUploading(true);
    setProgress(0);

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setUploading(false);
          triggerStructResult([
            { id: 1, name: 'Computer Networks', category: 'Computer Science', availability: 'Available', confidence: 98, status: 'Ready' },
            { id: 2, name: 'Operating Systems Concepts', category: 'Computer Science', availability: 'Borrowed', confidence: 94, status: 'Ready' },
            { id: 3, name: 'Introduction to Algorithms', category: 'Mathematics', availability: 'Available', confidence: 96, status: 'Ready' },
            { id: 4, name: 'Design Patterns', category: 'Software Engineering', availability: 'Available', confidence: 67, status: 'Needs Review' }
          ]);
          return 100;
        }
        return prev + 20;
      });
    }, 300);
  };

  const handleStructureText = () => {
    if (!unstructuredText.trim()) return;
    setStructuring(true);
    setTimeout(() => {
      setStructuring(false);
      triggerStructResult([
        { id: 1, name: 'Computer Networks', category: 'Computer Science', availability: 'Available', confidence: 98, status: 'Ready' },
        { id: 2, name: 'Operating Systems Concepts', category: 'Computer Science', availability: 'Available', confidence: 94, status: 'Ready' },
        { id: 3, name: 'Introduction to Algorithms', category: 'Mathematics', availability: 'Borrowed', confidence: 96, status: 'Ready' }
      ]);
    }, 1500);
  };

  const triggerStructResult = (data) => {
    setRecords(data);
    setShowValidation(true);
    showToast(`${data.length} records detected and structured.`);
  };

  const showToast = (msg) => {
    setNotification(msg);
    setTimeout(() => setNotification(null), 4000);
  };

  const handleSave = () => {
    showToast("Records saved successfully to the database.");
    setShowValidation(false);
    setRecords([]);
  };

  return (
    <div className="space-y-6 pb-12">
      {notification && (
        <div className="fixed bottom-6 right-6 bg-[#17152A] text-white px-4 py-3 rounded-lg shadow-xl border border-white/10 flex items-center gap-2 z-50 animate-bounce">
          <CheckCircle2 className="w-5 h-5 text-[#16A34A]" />
          <span className="text-sm font-medium">{notification}</span>
        </div>
      )}

      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-[#17152A]">Data Management</h2>
          <p className="text-[#747184] text-sm mt-1">Import, normalize, and manage library records.</p>
        </div>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-white border border-[#E8E7EF] rounded-lg text-sm font-medium text-[#17152A] hover:bg-[#F7F7FA]">
            Upload CSV
          </button>
          <button className="px-4 py-2 bg-[#6D4AFF] text-white rounded-lg text-sm font-medium hover:bg-[#5427E6]">
            Add Data
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-xl border border-[#E8E7EF] shadow-sm">
          <p className="text-sm text-[#747184] font-medium">Total Books</p>
          <p className="text-3xl font-bold text-[#17152A] mt-2">1,204</p>
        </div>
        <div className="bg-white p-5 rounded-xl border border-[#E8E7EF] shadow-sm">
          <p className="text-sm text-[#747184] font-medium">Available Books</p>
          <p className="text-3xl font-bold text-[#17152A] mt-2">876</p>
        </div>
        <div className="bg-white p-5 rounded-xl border border-[#E8E7EF] shadow-sm">
          <p className="text-sm text-[#747184] font-medium">Data Quality</p>
          <p className="text-3xl font-bold text-[#16A34A] mt-2">94.8%</p>
        </div>
      </div>

      {/* CSV Uploader */}
      <div className="bg-white p-6 rounded-xl border border-[#E8E7EF] shadow-sm">
        <h3 className="text-lg font-bold text-[#17152A] mb-1">Import Library Data</h3>
        <p className="text-sm text-[#747184] mb-4">Upload a CSV containing library records. LibraAI will automatically detect columns, normalize values, and convert the data into a structured book dataset.</p>

        <div className="border-2 border-dashed border-[#E8E7EF] hover:border-[#6D4AFF] rounded-xl p-8 text-center bg-[#F7F7FA] transition-colors cursor-pointer relative">
          <input type="file" accept=".csv" onChange={handleFileUpload} className="absolute inset-0 opacity-0 cursor-pointer" />
          <Upload className="w-10 h-10 text-[#6D4AFF] mx-auto mb-3" />
          <p className="text-sm font-semibold text-[#17152A]">Drag & drop your CSV here, or <span className="text-[#6D4AFF] underline">Browse Files</span></p>
          <p className="text-xs text-[#747184] mt-2">Supported format: CSV • Max file size: 10 MB</p>
        </div>

        {file && (
          <div className="mt-4 p-4 bg-[#F7F7FA] rounded-lg border border-[#E8E7EF] flex items-center justify-between">
            <div className="flex items-center gap-3">
              <FileText className="w-6 h-6 text-[#6D4AFF]" />
              <div>
                <p className="text-sm font-medium text-[#17152A]">{file.name}</p>
                <p className="text-xs text-[#747184]">{file.size || '2.4 MB'}</p>
              </div>
            </div>
            {uploading ? (
              <div className="w-32">
                <div className="flex justify-between text-xs text-[#747184] mb-1">
                  <span>Uploading...</span>
                  <span>{progress}%</span>
                </div>
                <div className="w-full bg-[#E8E7EF] h-1.5 rounded-full overflow-hidden">
                  <div className="bg-[#6D4AFF] h-full transition-all duration-200" style={{ width: `${progress}%` }}></div>
                </div>
              </div>
            ) : (
              <span className="text-xs font-bold text-[#16A34A] bg-[#16A34A]/10 px-2.5 py-1 rounded-full">Uploaded</span>
            )}
          </div>
        )}
      </div>

      {/* Unstructured Data */}
      <div className="bg-white p-6 rounded-xl border border-[#E8E7EF] shadow-sm">
        <h3 className="text-lg font-bold text-[#17152A] mb-1 flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-[#6D4AFF]" /> AI Data Structuring
        </h3>
        <p className="text-sm text-[#747184] mb-4">Paste unstructured library data and LibraAI will extract the relevant book information automatically.</p>

        <textarea
          rows={4}
          placeholder={`Paste library information here...\n\nExample:\nComputer Networks by Andrew Tanenbaum\nComputer Science\nCurrently available`}
          value={unstructuredText}
          onChange={(e) => setUnstructuredText(e.target.value)}
          className="w-full bg-[#F7F7FA] border border-[#E8E7EF] rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#6D4AFF]"
        />

        <div className="mt-3 flex justify-end">
          <button
            onClick={handleStructureText}
            disabled={structuring || !unstructuredText.trim()}
            className="flex items-center gap-2 px-5 py-2.5 bg-[#6D4AFF] text-white rounded-lg text-sm font-medium hover:bg-[#5427E6] disabled:opacity-50 transition-colors"
          >
            {structuring ? <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div> : <Sparkles className="w-4 h-4" />}
            Structure Data
          </button>
        </div>
      </div>

      {/* Preview and Validation */}
      {showValidation && (
        <div className="bg-white p-6 rounded-xl border border-[#E8E7EF] shadow-sm space-y-4 animate-in fade-in duration-300">
          <div className="flex justify-between items-center border-b border-[#E8E7EF] pb-4">
            <div>
              <h3 className="text-lg font-bold text-[#17152A]">Structured Records</h3>
              <p className="text-xs text-[#747184]">Review extracted data before saving into production database.</p>
            </div>
            <div className="flex gap-2">
              <button onClick={() => setShowValidation(false)} className="px-3 py-1.5 border border-[#E8E7EF] rounded-lg text-sm text-[#747184] hover:bg-[#F7F7FA]">
                Cancel
              </button>
              <button onClick={handleSave} className="px-4 py-1.5 bg-[#16A34A] text-white rounded-lg text-sm font-medium hover:bg-green-700">
                Approve All
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[#E8E7EF] text-xs font-semibold text-[#747184] uppercase">
                  <th className="py-3 px-4">Book Name</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Availability</th>
                  <th className="py-3 px-4">Confidence</th>
                  <th className="py-3 px-4">Validation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E8E7EF] text-sm">
                {records.map((r, idx) => (
                  <tr key={r.id}>
                    <td className="py-3 px-4">
                      <input 
                        type="text" 
                        value={r.name} 
                        onChange={(e) => {
                          const updated = [...records];
                          updated[idx].name = e.target.value;
                          setRecords(updated);
                        }}
                        className="bg-[#F7F7FA] border border-[#E8E7EF] rounded px-2 py-1 text-sm font-medium text-[#17152A] w-full"
                      />
                    </td>
                    <td className="py-3 px-4">
                      <input 
                        type="text" 
                        value={r.category} 
                        onChange={(e) => {
                          const updated = [...records];
                          updated[idx].category = e.target.value;
                          setRecords(updated);
                        }}
                        className="bg-[#F7F7FA] border border-[#E8E7EF] rounded px-2 py-1 text-sm text-[#747184] w-full"
                      />
                    </td>
                    <td className="py-3 px-4">
                      <select 
                        value={r.availability}
                        onChange={(e) => {
                          const updated = [...records];
                          updated[idx].availability = e.target.value;
                          setRecords(updated);
                        }}
                        className="bg-[#F7F7FA] border border-[#E8E7EF] rounded px-2 py-1 text-sm text-[#17152A]"
                      >
                        <option>Available</option>
                        <option>Borrowed</option>
                        <option>Reserved</option>
                      </select>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                        r.confidence >= 95 ? 'bg-[#16A34A]/10 text-[#16A34A]' :
                        r.confidence >= 80 ? 'bg-[#F59E0B]/10 text-[#F59E0B]' : 'bg-[#BA1A1A]/10 text-[#BA1A1A]'
                      }`}>
                        {r.confidence}%
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      {r.confidence >= 80 ? (
                        <span className="flex items-center gap-1 text-xs text-[#16A34A] font-medium"><Check className="w-4 h-4" /> Valid</span>
                      ) : (
                        <span className="flex items-center gap-1 text-xs text-[#F59E0B] font-medium"><AlertTriangle className="w-4 h-4" /> Review</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex justify-end gap-2 pt-4 border-t border-[#E8E7EF]">
            <button onClick={handleSave} className="px-5 py-2 bg-[#6D4AFF] text-white rounded-lg text-sm font-medium hover:bg-[#5427E6]">
              Save Valid Records
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataManagement;
