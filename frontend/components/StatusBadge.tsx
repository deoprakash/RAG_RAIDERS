'use client';
import { Loader2 } from 'lucide-react';

interface StatusBadgeProps {
  status: 'PASSED' | 'FAILED' | 'RUNNING';
  size?: 'sm' | 'md' | 'lg';
}

export default function StatusBadge({ status, size = 'md' }: StatusBadgeProps) {
  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-3 py-1',
    lg: 'text-base px-4 py-2',
  };

  const iconSizes = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
  };

  if (status === 'PASSED') {
    return (
      <div className={`inline-flex items-center gap-2 bg-green-500/20 text-green-400 border border-green-500/40 rounded-full font-semibold ${sizeClasses[size]}`}>
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
        </span>
        PASSED
      </div>
    );
  }

  if (status === 'FAILED') {
    return (
      <div className={`inline-flex items-center gap-2 bg-red-500/20 text-red-400 border border-red-500/40 rounded-full font-semibold ${sizeClasses[size]}`}>
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
        </span>
        FAILED
      </div>
    );
  }

  // RUNNING
  return (
    <div className={`inline-flex items-center gap-2 bg-amber-500/20 text-amber-400 border border-amber-500/40 rounded-full font-semibold ${sizeClasses[size]}`}>
      <Loader2 className={`animate-spin ${iconSizes[size]}`} />
      RUNNING
    </div>
  );
}
