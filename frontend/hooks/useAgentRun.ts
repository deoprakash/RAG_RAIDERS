'use client';
import { useEffect, useRef } from 'react';
import axios from 'axios';
import { useAgentStore } from '@/store/agentStore';
import { mockResults, mockLogs } from '@/utils/mockData';

export function useAgentRun() {
  const store = useAgentStore();
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const startRef = useRef<number>(0);

  const runAgent = async () => {
    if (!store.repoUrl || !store.teamName || !store.leaderName) return;

    store.startRun();
    startRef.current = Date.now();

    timerRef.current = setInterval(() => {
      store.setElapsed(Math.floor((Date.now() - startRef.current) / 1000));
    }, 1000);

    // ── DEMO MODE ──────────────────────────────────────────
    if (store.demoMode) {
      for (const log of mockLogs) {
        await new Promise((r) => setTimeout(r, 850));
        store.appendLog(log);
      }
      await new Promise((r) => setTimeout(r, 500));
      if (timerRef.current) clearInterval(timerRef.current);
      store.setResults(mockResults);
      return;
    }

    // ── REAL MODE ───────────────────────────────────────────
    try {
      const { data } = await axios.post('/api/run', {
        repoUrl: store.repoUrl,
        teamName: store.teamName,
        leaderName: store.leaderName,
      });
      const runId: string = data.run_id;

      const poll = setInterval(async () => {
        try {
          const { data: statusData } = await axios.get(`/api/run/${runId}/status`);
          if (statusData.log) store.appendLog(statusData.log);

          if (
            statusData.final_status === 'PASSED' ||
            statusData.final_status === 'FAILED'
          ) {
            clearInterval(poll);
            if (timerRef.current) clearInterval(timerRef.current);
            const { data: results } = await axios.get(`/api/run/${runId}/results`);
            store.setResults(results);
          }
        } catch {
          clearInterval(poll);
          if (timerRef.current) clearInterval(timerRef.current);
          store.setStatus('error');
        }
      }, 2000);
    } catch {
      if (timerRef.current) clearInterval(timerRef.current);
      store.setStatus('error');
    }
  };

  useEffect(() => () => { if (timerRef.current) clearInterval(timerRef.current); }, []);
  return { runAgent };
}
