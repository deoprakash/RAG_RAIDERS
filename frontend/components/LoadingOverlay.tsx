'use client';
import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useAgentStore } from '@/store/agentStore';
import { formatDuration } from '@/utils/formatters';

export default function LoadingOverlay() {
  const { isRunning, logs, elapsed } = useAgentStore();
  const logEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Auto-scroll to bottom
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  if (!isRunning) return null;

  return (
    <div className="fixed inset-0 z-50 bg-[#0A0E1A]/90 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="w-full max-w-xl bg-[#111827] border border-[#1E2D45] rounded-xl overflow-hidden">
        {/* Terminal Header */}
        <div className="bg-[#1A2235] px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#EF4444]"></div>
            <div className="w-3 h-3 rounded-full bg-[#F59E0B]"></div>
            <div className="w-3 h-3 rounded-full bg-[#10B981]"></div>
            <span className="font-mono text-xs text-[#6B7280] ml-2">agent-runner — zsh</span>
          </div>
          <div className="font-mono text-xs text-amber-400">
            ⏱ {formatDuration(elapsed)}
          </div>
        </div>

        {/* Terminal Body */}
        <div className="bg-[#0A0E1A] p-4 h-72 overflow-y-auto font-mono text-sm">
          {logs.map((log, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index, duration: 0.3 }}
              className="mb-1"
            >
              <span className="text-[#6B7280]">[{log.time}]</span> <span className="text-[#F9FAFB]">{log.message}</span>
            </motion.div>
          ))}
          <div ref={logEndRef} />
        </div>

        {/* Progress Bar */}
        <div className="h-1 bg-[#1A2235] w-full relative overflow-hidden">
          <motion.div
            className="h-full"
            style={{ background: 'linear-gradient(to right, #3B82F6, #8B5CF6)' }}
            initial={{ width: '0%' }}
            animate={{ width: `${Math.min((elapsed / 90) * 100, 95)}%` }}
            transition={{ duration: 1 }}
          />
        </div>

        {/* Cancel Hint */}
        <div className="bg-[#111827] py-3 text-center">
          <p className="text-xs text-[#6B7280]">Processing... please wait</p>
        </div>
      </div>
    </div>
  );
}
