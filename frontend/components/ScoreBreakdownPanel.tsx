'use client';
import { Trophy } from 'lucide-react';
import { BarChart, Bar, XAxis, ResponsiveContainer, Tooltip, Cell } from 'recharts';
import type { AgentResults } from '@/types';

interface ScoreBreakdownPanelProps {
  results: AgentResults;
}

export default function ScoreBreakdownPanel({ results }: ScoreBreakdownPanelProps) {
  const { score } = results;
  const hasSpeedBonus = score.speed_bonus > 0;

  const chartData = [
    { name: 'Base', value: score.base },
    { name: 'Speed', value: score.speed_bonus },
    { name: 'Penalty', value: score.penalty },
  ];

  const barColors = ['#6366F1', '#10B981', '#EF4444'];

  return (
    <div
      className="bg-[#1A2235] border border-[#1E2D45] rounded-2xl p-6"
      style={{ boxShadow: '0 -2px 20px rgba(139,92,246,0.2)' }}
    >
      {/* Header */}
      <div className="flex items-center gap-2 mb-6">
        <Trophy className="w-6 h-6 text-[#F59E0B]" />
        <h2 className="text-2xl font-bold text-[#F9FAFB]">Score Breakdown</h2>
      </div>

      {/* Score Items */}
      <div className="space-y-3 mb-4">
        <div className="flex items-center justify-between">
          <span className="text-[#9CA3AF]">Base Score</span>
          <span className="text-[#F9FAFB] font-semibold">{score.base} pts</span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-[#9CA3AF]">Speed Bonus</span>
          <span className={`font-semibold ${score.speed_bonus > 0 ? 'text-[#10B981]' : 'text-[#9CA3AF]'}`}>
            +{score.speed_bonus} pts
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-[#9CA3AF]">Efficiency Penalty</span>
          <span className={`font-semibold ${score.penalty > 0 ? 'text-[#EF4444]' : 'text-[#10B981]'}`}>
            -{score.penalty} pts
          </span>
        </div>

        <div className="border-t border-[#1E2D45] my-3"></div>

        <div className="flex items-center justify-between">
          <span className="text-[#F9FAFB] font-bold text-lg">FINAL SCORE</span>
          <span className="gradient-text text-4xl font-bold">{score.total}</span>
        </div>

        {hasSpeedBonus && (
          <p className="text-xs text-[#10B981] mt-2">
            ✓ {'< 5 min bonus applied'}
          </p>
        )}
      </div>

      {/* Chart */}
      <div className="mt-6">
        <ResponsiveContainer width="100%" height={120}>
          <BarChart data={chartData} layout="vertical">
            <XAxis type="number" hide />
            <Tooltip
              contentStyle={{
                backgroundColor: '#111827',
                border: '1px solid #1E2D45',
                borderRadius: '8px',
                color: '#F9FAFB',
              }}
            />
            <Bar dataKey="value" radius={[4, 4, 0, 0]} animationBegin={0} animationDuration={1500}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={barColors[index]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
