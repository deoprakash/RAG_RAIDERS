'use client';
import { AlertTriangle } from 'lucide-react';
import { useAgentStore } from '@/store/agentStore';
import RunSummaryCard from './RunSummaryCard';
import ScoreBreakdownPanel from './ScoreBreakdownPanel';
import CICDTimeline from './CICDTimeline';
import FixesTable from './FixesTable';

export default function Dashboard() {
  const { status, results, reset } = useAgentStore();

  if (status === 'idle') return null;

  if (status === 'error') {
    return (
      <div className="max-w-2xl mx-auto mt-12">
        <div className="bg-[#111827] border border-[#EF4444]/30 rounded-2xl p-8 text-center">
          <AlertTriangle className="w-16 h-16 text-[#EF4444] mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-[#EF4444] mb-2">Agent Error</h2>
          <p className="text-[#9CA3AF] mb-6">
            Agent encountered an error. Please try again.
          </p>
          <button
            onClick={reset}
            style={{ background: 'linear-gradient(135deg, #3B82F6, #8B5CF6)' }}
            className="px-6 py-3 rounded-lg font-semibold text-white hover:scale-105 transition-transform"
          >
            Reset and Try Again
          </button>
        </div>
      </div>
    );
  }

  if (status === 'complete' && results) {
    return (
      <div className="flex flex-col gap-6 mt-8">
        <RunSummaryCard results={results} />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ScoreBreakdownPanel results={results} />
          <CICDTimeline runs={results.cicd_runs} />
        </div>

        <FixesTable fixes={results.fixes} />
      </div>
    );
  }

  return null;
}
