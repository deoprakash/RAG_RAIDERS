'use client';
import { useEffect, useRef } from 'react';
import axios from 'axios';
import { useAgentStore } from '@/store/agentStore';

function getLogTime() {
  const now = new Date();
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  return `${minutes}:${seconds}`;
}

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

    try {
      store.appendLog({ time: getLogTime(), message: '🚀 Starting agent run...' });
      store.appendLog({ time: getLogTime(), message: '🔗 Connecting to backend...' });

      const { data: results } = await axios.post('/api/run', {
        repoUrl: store.repoUrl,
        teamName: store.teamName,
        leaderName: store.leaderName,
      });

      store.appendLog({
        time: getLogTime(),
        message: `✅ Agent run finished with status: ${results.final_status}`,
      });

      if (timerRef.current) clearInterval(timerRef.current);
      store.setResults(results);
    } catch (error) {
      const message = axios.isAxiosError(error)
        ? (error.response?.data?.message as string | undefined) ?? error.message
        : 'Backend request failed';

      store.appendLog({ time: getLogTime(), message: `❌ ${message}` });
      if (timerRef.current) clearInterval(timerRef.current);
      store.setStatus('error');
    }
  };

  useEffect(() => () => { if (timerRef.current) clearInterval(timerRef.current); }, []);
  return { runAgent };
}
