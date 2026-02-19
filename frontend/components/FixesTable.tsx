'use client';
import { CheckCircle2, XCircle, Download } from 'lucide-react';
import { motion } from 'framer-motion';
import type { Fix, BugType } from '@/types';

interface FixesTableProps {
  fixes: Fix[];
}

const bugTypeColors: Record<BugType, string> = {
  LINTING: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
  SYNTAX: 'bg-red-500/20 text-red-400 border-red-500/30',
  LOGIC: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  TYPE_ERROR: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  IMPORT: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
  INDENTATION: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
};

export default function FixesTable({ fixes }: FixesTableProps) {
  const exportCSV = () => {
    if (fixes.length === 0) return;

    const headers = ['File', 'Bug Type', 'Line #', 'Commit Message', 'Status'];
    const rows = fixes.map((fix) => [
      fix.file,
      fix.bug_type,
      fix.line_number.toString(),
      fix.commit_message,
      fix.status,
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map((row) => row.map((cell) => `"${cell}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'agent-fixes.csv';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-[#111827] border border-[#1E2D45] rounded-2xl p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-[#F9FAFB]">Fixes Applied</h2>
        <button
          onClick={exportCSV}
          disabled={fixes.length === 0}
          className="flex items-center gap-2 bg-[#1A2235] hover:bg-[#1E2D45] border border-[#1E2D45] rounded-lg px-4 py-2 text-sm text-[#F9FAFB] transition-colors"
        >
          <Download className="w-4 h-4" />
          Export CSV
        </button>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-[#1A2235] sticky top-0 z-10">
            <tr>
              <th className="text-left px-4 py-3 text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider">
                File
              </th>
              <th className="text-left px-4 py-3 text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider">
                Bug Type
              </th>
              <th className="text-center px-4 py-3 text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider">
                Line #
              </th>
              <th className="text-left px-4 py-3 text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider">
                Commit Message
              </th>
              <th className="text-center px-4 py-3 text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider">
                Status
              </th>
            </tr>
          </thead>
          <tbody>
            {fixes.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-[#9CA3AF] text-sm">
                  No fixes were applied in this run.
                </td>
              </tr>
            ) : fixes.map((fix, index) => (
              <motion.tr
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className={`hover:bg-[#1E2D45]/50 transition-colors ${
                  index % 2 === 0 ? 'bg-[#1A2235]/30' : ''
                }`}
              >
                <td className="px-4 py-3 font-mono text-sm text-[#F9FAFB]">{fix.file}</td>
                <td className="px-4 py-3">
                  <span
                    className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${
                      bugTypeColors[fix.bug_type]
                    }`}
                  >
                    {fix.bug_type}
                  </span>
                </td>
                <td className="px-4 py-3 font-mono text-[#06B6D4] text-center">{fix.line_number}</td>
                <td className="px-4 py-3 font-mono text-xs text-[#9CA3AF] max-w-xs truncate" title={fix.commit_message}>
                  {fix.commit_message}
                </td>
                <td className="px-4 py-3 text-center">
                  {fix.status === 'FIXED' ? (
                    <span className="inline-flex items-center gap-1 text-[#10B981] text-sm font-semibold">
                      <CheckCircle2 className="w-4 h-4" />
                      Fixed
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-[#EF4444] text-sm font-semibold">
                      <XCircle className="w-4 h-4" />
                      Failed
                    </span>
                  )}
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
