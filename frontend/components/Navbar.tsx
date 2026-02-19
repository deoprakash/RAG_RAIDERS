'use client';
import { useEffect, useState } from 'react';
import { Code2 } from 'lucide-react';

export default function Navbar() {
  const [time, setTime] = useState('');

  useEffect(() => {
    const updateTime = () => {
      setTime(new Date().toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      }));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <nav className="sticky top-0 z-50 backdrop-blur-md bg-[#0A0E1A]/80 border-b border-[#1E2D45] h-16">
      <div className="max-w-7xl mx-auto px-4 h-full flex items-center justify-between">
        {/* Left: Logo */}
        <div className="flex items-center gap-3">
          <Code2 className="w-6 h-6 text-[#3B82F6]" />
          <span className="text-xl font-bold gradient-text">RIFT Agent</span>
        </div>

        {/* Center: Tagline (hidden on mobile) */}
        <div className="hidden md:block">
          <span className="text-xs tracking-[0.2em] text-[#6B7280] uppercase">
            Autonomous CI/CD Healing Agent
          </span>
        </div>

        {/* Right: Clock + Badge */}
        <div className="flex items-center gap-4">
          <span className="font-mono text-sm text-[#9CA3AF]">{time}</span>
          <span className="bg-amber-500/20 text-amber-400 border border-amber-500/40 px-3 py-1 rounded-full text-xs font-semibold">
            RIFT 2026
          </span>
        </div>
      </div>
    </nav>
  );
}
