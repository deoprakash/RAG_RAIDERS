'use client';
import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ExternalLink } from 'lucide-react';
import confetti from 'canvas-confetti';
import StatusBadge from './StatusBadge';
import { formatDuration } from '@/utils/formatters';
import type { AgentResults } from '@/types';

interface RunSummaryCardProps {
  results: AgentResults;
}

export default function RunSummaryCard({ results }: RunSummaryCardProps) {
  const [failuresCount, setFailuresCount] = useState(0);
  const [fixesCount, setFixesCount] = useState(0);
  const [iterationsCount, setIterationsCount] = useState(0);

  useEffect(() => {
    // Fire confetti on PASSED
    if (results.final_status === 'PASSED') {
      confetti({
        particleCount: 150,
        spread: 80,
        origin: { y: 0.6 },
        colors: ['#3B82F6', '#8B5CF6', '#10B981', '#06B6D4'],
      });
    }

    // Animate counts
    const duration = 1500;
    const steps = 60;
    const interval = duration / steps;

    let step = 0;
    const timer = setInterval(() => {
      step++;
      const progress = step / steps;
      setFailuresCount(Math.floor(results.total_failures * progress));
      setFixesCount(Math.floor(results.total_fixes * progress));
      setIterationsCount(Math.floor(results.cicd_runs.length * progress));

      if (step >= steps) {
        clearInterval(timer);
        setFailuresCount(results.total_failures);
        setFixesCount(results.total_fixes);
        setIterationsCount(results.cicd_runs.length);
      }
    }, interval);

    return () => clearInterval(timer);
  }, [results]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-[#111827] border border-[#1E2D45] rounded-2xl p-6 glow-blue"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-[#F9FAFB]">Run Summary</h2>
        <StatusBadge status={results.final_status} size="lg" />
      </div>

      {/* 2-column grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
        {/* Left column */}
        <div className="space-y-3">
          <div>
            <span className="text-xs text-[#6B7280] uppercase tracking-wider">Repository</span>
            <div className="flex items-center gap-2 mt-1">
              <a
                href={results.repo_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[#3B82F6] hover:text-[#60A5FA] transition-colors truncate max-w-xs flex items-center gap-1"
              >
                <span className="truncate">{results.repo_url}</span>
                <ExternalLink className="w-3 h-3 shrink-0" />
              </a>
            </div>
          </div>

          <div>
            <span className="text-xs text-[#6B7280] uppercase tracking-wider">Team</span>
            <p className="font-bold text-[#F9FAFB] mt-1">{results.team_name}</p>
          </div>

          <div>
            <span className="text-xs text-[#6B7280] uppercase tracking-wider">Leader</span>
            <p className="font-bold text-[#F9FAFB] mt-1">{results.leader_name}</p>
          </div>

          <div>
            <span className="text-xs text-[#6B7280] uppercase tracking-wider">Branch</span>
            <div className="font-mono text-[#06B6D4] text-sm bg-[#0A0E1A] border border-[#06B6D4]/30 rounded px-2 py-1 inline-block mt-1">
              {results.branch}
            </div>
          </div>

          <div>
            <span className="text-xs text-[#6B7280] uppercase tracking-wider">Time Taken</span>
            <p className="font-bold text-amber-400 mt-1">
              ⏱ {formatDuration(results.duration_seconds)}
            </p>
          </div>
        </div>

        {/* Right column - Stats */}
        <div className="grid grid-cols-1 gap-4">
          <div className="bg-[#0A0E1A] rounded-xl p-4 text-center">
            <div className="text-3xl font-bold text-[#EF4444]">{failuresCount}</div>
            <div className="text-xs text-[#6B7280] uppercase tracking-wider mt-1">Failures Detected</div>
          </div>

          <div className="bg-[#0A0E1A] rounded-xl p-4 text-center">
            <div className="text-3xl font-bold text-[#10B981]">{fixesCount}</div>
            <div className="text-xs text-[#6B7280] uppercase tracking-wider mt-1">Fixes Applied</div>
          </div>

          <div className="bg-[#0A0E1A] rounded-xl p-4 text-center">
            <div className="text-3xl font-bold text-[#06B6D4]">{iterationsCount}</div>
            <div className="text-xs text-[#6B7280] uppercase tracking-wider mt-1">CI/CD Iterations</div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
