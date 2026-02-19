export const toBranchName = (team: string, leader: string): string => {
  if (!team && !leader) return '';
  const normalize = (value: string) =>
    value
      .trim()
      .toUpperCase()
      .replace(/\s+/g, '_')
      .replace(/[^A-Z0-9_]/g, '')
      .replace(/_+/g, '_')
      .replace(/^_|_$/g, '');

  const safeTeam = normalize(team);
  const safeLeader = normalize(leader);
  return `${safeTeam}_${safeLeader}_AI_Fix`;
};

export const formatDuration = (seconds: number): string => {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}m ${s.toString().padStart(2, '0')}s`;
};

export const formatTimestamp = (iso: string): string =>
  new Date(iso).toLocaleTimeString('en-IN', {
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  });

export const calcScore = (durationSeconds: number, totalCommits: number) => {
  const base = 100;
  const speedBonus = durationSeconds < 300 ? 10 : 0;
  const efficiencyPenalty = Math.max(0, totalCommits - 20) * 2;
  return {
    base,
    speedBonus,
    efficiencyPenalty,
    total: base + speedBonus - efficiencyPenalty,
  };
};
