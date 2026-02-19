'use client';
import { GitBranch, CheckCircle2, XCircle, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import StatusBadge from './StatusBadge';
import { formatTimestamp } from '@/utils/formatters';
import type { CICDRun } from '@/types';

interface CICDTimelineProps {
  runs: CICDRun[];
}

export default function CICDTimeline({ runs }: CICDTimelineProps) {
  const maxRetries = 5;
  const hasRuns = runs.length > 0;
  const finalRun = runs[runs.length - 1];
  const allPassed = finalRun?.status === 'PASSED';

  return (
    <div className="bg-[#111827] border border-[#1E2D45] rounded-2xl p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <GitBranch className="w-6 h-6 text-[#3B82F6]" />
          <h2 className="text-2xl font-bold text-[#F9FAFB]">CI/CD Pipeline Timeline</h2>
        </div>
        
        {/* Retry Counter */}
        <div className="flex items-center gap-2">
          <div className="flex gap-1">
            {Array.from({ length: maxRetries }).map((_, i) => (
              <div
                key={i}
                className={`w-3 h-3 rounded-full ${
                  i < runs.length
                    ? 'bg-[#3B82F6]'
                    : 'bg-[#1E2D45] border border-[#1E2D45]'
                }`}
              />
            ))}
          </div>
          <span className="text-xs text-[#9CA3AF]">
            {runs.length} / {maxRetries} retries used
          </span>
        </div>
      </div>

      {/* Timeline */}
      <div className="space-y-0">
        {hasRuns ? runs.map((run, index) => (
          <div key={index} className="relative">
            {/* Node */}
            <div className="flex items-start gap-4">
              {/* Circle + Connector */}
              <div className="flex flex-col items-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: index * 0.2, duration: 0.3 }}
                  className={`w-10 h-10 rounded-full flex items-center justify-center border-2 ${
                    run.status === 'PASSED'
                      ? 'border-[#10B981] bg-[#10B981]/20'
                      : run.status === 'FAILED'
                      ? 'border-[#EF4444] bg-[#EF4444]/20'
                      : 'border-[#F59E0B] bg-[#F59E0B]/20'
                  }`}
                >
                  {run.status === 'PASSED' && <CheckCircle2 className="w-5 h-5 text-[#10B981]" />}
                  {run.status === 'FAILED' && <XCircle className="w-5 h-5 text-[#EF4444]" />}
                  {run.status === 'RUNNING' && <Loader2 className="w-5 h-5 text-[#F59E0B] animate-spin" />}
                </motion.div>

                {/* Connector line (if not last) */}
                {index < runs.length - 1 && (
                  <motion.div
                    initial={{ scaleY: 0 }}
                    animate={{ scaleY: 1 }}
                    transition={{ delay: index * 0.2 + 0.3, duration: 0.3 }}
                    className={`w-0.5 h-12 ${
                      run.status === 'PASSED' ? 'bg-[#10B981]' : 'bg-[#EF4444]'
                    }`}
                    style={{ originY: 0 }}
                  />
                )}
              </div>

              {/* Content */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.2, duration: 0.3 }}
                className="flex-1 pb-8"
              >
                <div className="flex items-center gap-3 mb-1">
                  <span className="font-bold text-[#F9FAFB]">Run #{run.run_number}</span>
                  <StatusBadge status={run.status} size="sm" />
                </div>
                <p className="text-xs text-[#6B7280] mb-2">{formatTimestamp(run.timestamp)}</p>
                {run.status === 'FAILED' && (
                  <p className="text-xs text-[#EF4444]">
                    {run.failures_remaining} failures remaining
                  </p>
                )}
                {run.status === 'PASSED' && (
                  <p className="text-xs text-[#10B981]">
                    ✓ All tests passed
                  </p>
                )}
              </motion.div>
            </div>
          </div>
        )) : (
          <div className="bg-[#0A0E1A] border border-[#1E2D45] rounded-xl p-4 text-center">
            <p className="text-[#9CA3AF] text-sm">No CI/CD iterations recorded for this run.</p>
          </div>
        )}
      </div>

      {/* Bottom Outcome Banner */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: runs.length * 0.2 + 0.5 }}
        className="mt-4"
      >
        {!hasRuns ? (
          <div className="bg-[#1A2235]/60 border border-[#1E2D45] rounded-xl p-4 text-center">
            <p className="text-[#9CA3AF] font-semibold">
              ℹ️ Timeline will appear after CI/CD iterations are detected
            </p>
          </div>
        ) : allPassed ? (
          <div className="bg-[#10B981]/10 border border-[#10B981]/30 rounded-xl p-4 text-center">
            <p className="text-[#10B981] font-bold">
              🎉 ALL TESTS PASSED in {runs.length} iteration(s)
            </p>
          </div>
        ) : (
          <div className="bg-[#EF4444]/10 border border-[#EF4444]/30 rounded-xl p-4 text-center">
            <p className="text-[#EF4444] font-bold">
              ⚠️ MAX RETRIES REACHED — Manual review required
            </p>
          </div>
        )}
      </motion.div>
    </div>
  );
}
