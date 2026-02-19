'use client';
import Navbar from '@/components/Navbar';
import InputSection from '@/components/InputSection';
import LoadingOverlay from '@/components/LoadingOverlay';
import Dashboard from '@/components/Dashboard';
import { useAgentStore } from '@/store/agentStore';

export default function Home() {
  const { isRunning, status } = useAgentStore();
  return (
    <main className="min-h-screen bg-[#0A0E1A]">
      <Navbar />
      {isRunning && <LoadingOverlay />}
      <div className="max-w-6xl mx-auto px-4 pb-16">
        <InputSection />
        {status !== 'idle' && <Dashboard />}
      </div>
    </main>
  );
}

