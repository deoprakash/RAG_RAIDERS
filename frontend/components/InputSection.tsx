'use client';
import { useMemo } from 'react';
import { Github, Users, User, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { useAgentStore } from '@/store/agentStore';
import { useAgentRun } from '@/hooks/useAgentRun';
import { toBranchName } from '@/utils/formatters';

export default function InputSection() {
  const { repoUrl, teamName, leaderName, isRunning, setField } = useAgentStore();
  const { runAgent } = useAgentRun();

  const branchPreview = useMemo(() => {
    if (teamName && leaderName) {
      return toBranchName(teamName, leaderName);
    }
    return '';
  }, [teamName, leaderName]);

  const handleRun = () => {
    if (!repoUrl || !teamName || !leaderName) return;
    runAgent();
  };

  const isFormValid = repoUrl && teamName && leaderName;

  return (
    <section className="py-16 px-4 relative">
      {/* Radial glow background */}
      <div className="absolute inset-0 flex justify-center overflow-hidden pointer-events-none">
        <div
          className="w-150 h-100 opacity-20"
          style={{
            background: 'radial-gradient(ellipse at 50% 0%, rgba(59,130,246,0.4), transparent 70%)',
          }}
        />
      </div>

      <div className="max-w-2xl mx-auto bg-[#111827] border border-[#1E2D45] rounded-2xl p-8 relative z-10">
        {/* Heading */}
        <h1 className="text-3xl font-bold gradient-text text-center mb-2">
          Autonomous CI/CD Healing Agent
        </h1>
        <p className="text-[#9CA3AF] text-center mb-8">
          Paste a GitHub repo URL. The agent clones, analyzes, fixes, and pushes.
        </p>

        {/* Inputs */}
        <div className="space-y-5">
          {/* Repo URL */}
          <div>
            <label className="block text-sm font-medium text-[#F9FAFB] mb-2">
              <Github className="inline w-4 h-4 mr-2" />
              GitHub Repo URL
            </label>
            <input
              type="text"
              value={repoUrl}
              onChange={(e) => setField('repoUrl', e.target.value)}
              placeholder="https://github.com/org/repo"
              className="bg-[#0A0E1A] border border-[#1E2D45] rounded-lg px-4 py-3 text-[#F9FAFB] focus:border-[#3B82F6] focus:ring-1 focus:ring-[#3B82F6] outline-none w-full transition-all"
              disabled={isRunning}
            />
          </div>

          {/* Team Name */}
          <div>
            <label className="block text-sm font-medium text-[#F9FAFB] mb-2">
              <Users className="inline w-4 h-4 mr-2" />
              Team Name
            </label>
            <input
              type="text"
              value={teamName}
              onChange={(e) => setField('teamName', e.target.value)}
              placeholder="RIFT ORGANISERS"
              className="bg-[#0A0E1A] border border-[#1E2D45] rounded-lg px-4 py-3 text-[#F9FAFB] focus:border-[#3B82F6] focus:ring-1 focus:ring-[#3B82F6] outline-none w-full transition-all"
              disabled={isRunning}
            />
          </div>

          {/* Leader Name */}
          <div>
            <label className="block text-sm font-medium text-[#F9FAFB] mb-2">
              <User className="inline w-4 h-4 mr-2" />
              Team Leader Name
            </label>
            <input
              type="text"
              value={leaderName}
              onChange={(e) => setField('leaderName', e.target.value)}
              placeholder="Saiyam Kumar"
              className="bg-[#0A0E1A] border border-[#1E2D45] rounded-lg px-4 py-3 text-[#F9FAFB] focus:border-[#3B82F6] focus:ring-1 focus:ring-[#3B82F6] outline-none w-full transition-all"
              disabled={isRunning}
            />
          </div>
        </div>

        {/* Branch Preview */}
        {branchPreview && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="mt-4"
          >
            <p className="text-xs text-[#6B7280] mb-1">Branch will be created:</p>
            <div className="font-mono text-[#06B6D4] bg-[#0A0E1A] border border-[#1E2D45] rounded px-3 py-2 text-sm">
              {branchPreview}
            </div>
          </motion.div>
        )}

        {/* Run Button */}
        <button
          onClick={handleRun}
          disabled={!isFormValid || isRunning}
          style={
            isFormValid && !isRunning
              ? { background: 'linear-gradient(135deg, #3B82F6, #8B5CF6)' }
              : undefined
          }
          className={`w-full h-12 rounded-xl font-semibold text-white mt-6 transition-all duration-200 ${
            isFormValid && !isRunning
              ? 'hover:scale-[1.02] active:scale-[0.98] shadow-lg hover:shadow-xl'
              : 'bg-[#1E2D45] cursor-not-allowed opacity-50'
          }`}
        >
          {isRunning ? (
            <span className="flex items-center justify-center gap-2">
              <Loader2 className="animate-spin w-5 h-5" />
              Running Agent...
            </span>
          ) : (
            '🚀 Run Agent'
          )}
        </button>

        {/* Disclaimer */}
        <p className="text-xs text-[#6B7280] text-center mt-3">
          Agent commits with [AI-AGENT] prefix and pushes to a new branch automatically.
        </p>
      </div>
    </section>
  );
}
