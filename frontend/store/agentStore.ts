'use client';
import { create } from 'zustand';
import type { AgentResults, LogLine, RunStatus } from '@/types';

interface AgentStore {
  repoUrl: string;
  teamName: string;
  leaderName: string;
  isRunning: boolean;
  logs: LogLine[];
  elapsed: number;
  results: AgentResults | null;
  status: RunStatus;
  demoMode: boolean;

  setField: (field: 'repoUrl' | 'teamName' | 'leaderName', value: string) => void;
  startRun: () => void;
  appendLog: (log: LogLine) => void;
  setResults: (results: AgentResults) => void;
  setElapsed: (s: number) => void;
  setStatus: (s: RunStatus) => void;
  toggleDemo: () => void;
  reset: () => void;
}

export const useAgentStore = create<AgentStore>((set) => ({
  repoUrl: '',
  teamName: '',
  leaderName: '',
  isRunning: false,
  logs: [],
  elapsed: 0,
  results: null,
  status: 'idle',
  demoMode: true, // DEFAULT TRUE so judges can see it immediately

  setField: (field, value) => set((s) => ({ ...s, [field]: value })),
  startRun: () =>
    set({ isRunning: true, status: 'running', logs: [], results: null, elapsed: 0 }),
  appendLog: (log) => set((s) => ({ logs: [...s.logs, log] })),
  setResults: (results) =>
    set({ results, isRunning: false, status: 'complete' }),
  setElapsed: (elapsed) => set({ elapsed }),
  setStatus: (status) => set({ status }),
  toggleDemo: () => set((s) => ({ demoMode: !s.demoMode })),
  reset: () =>
    set({ results: null, status: 'idle', logs: [], elapsed: 0, isRunning: false }),
}));
