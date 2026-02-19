import { NextRequest, NextResponse } from 'next/server';
import type { AgentResults, Fix, CICDRun, CICDStatus, BugType } from '@/types';

type BackendScore = {
  base?: number;
  speed_bonus?: number;
  penalty?: number;
  total?: number;
  final_score?: number;
};

type BackendFix = {
  file?: string;
  bug_type?: string;
  line_number?: number;
  commit_message?: string;
  status?: string;
};

type BackendTimeline = {
  iteration?: number;
  status?: string;
  timestamp?: string;
  failures_remaining?: number;
};

type BackendRunResult = {
  run_id?: string;
  repo_url?: string;
  team_name?: string;
  leader_name?: string;
  branch?: string;
  branch_name?: string;
  start_time?: string;
  end_time?: string;
  duration_seconds?: number;
  time_taken_seconds?: number;
  total_failures?: number;
  total_fixes?: number;
  fixes_applied?: number;
  total_commits?: number;
  final_status?: string;
  score?: BackendScore;
  fixes?: BackendFix[];
  cicd_runs?: BackendTimeline[];
  ci_cd_timeline?: BackendTimeline[];
};

const allowedBugTypes: BugType[] = [
  'LINTING',
  'SYNTAX',
  'LOGIC',
  'TYPE_ERROR',
  'IMPORT',
  'INDENTATION',
];

function toBugType(value: string | undefined): BugType {
  if (!value) return 'LOGIC';
  const upper = value.toUpperCase();
  return allowedBugTypes.includes(upper as BugType) ? (upper as BugType) : 'LOGIC';
}

function toFixStatus(value: string | undefined): 'FIXED' | 'FAILED' {
  return value?.toUpperCase() === 'FIXED' ? 'FIXED' : 'FAILED';
}

function toCICDStatus(value: string | undefined): CICDStatus {
  const upper = value?.toUpperCase();
  if (upper === 'PASSED' || upper === 'FAILED' || upper === 'RUNNING') return upper;
  return 'FAILED';
}

function normalizeResults(raw: BackendRunResult): AgentResults {
  const nowIso = new Date().toISOString();
  const score = raw.score ?? {};
  const timeline = raw.cicd_runs ?? raw.ci_cd_timeline ?? [];
  const fixes = raw.fixes ?? [];
  const totalFixes = raw.total_fixes ?? raw.fixes_applied ?? fixes.length;
  const durationSeconds =
    raw.duration_seconds ??
    (typeof raw.time_taken_seconds === 'number'
      ? Math.round(raw.time_taken_seconds)
      : 0);

  const normalizedFixes: Fix[] = fixes.map((fix) => ({
    file: fix.file ?? 'unknown',
    bug_type: toBugType(fix.bug_type),
    line_number: typeof fix.line_number === 'number' ? fix.line_number : 0,
    commit_message: fix.commit_message ?? '',
    status: toFixStatus(fix.status),
  }));

  const normalizedRuns: CICDRun[] = timeline.map((run, index) => ({
    run_number: typeof run.iteration === 'number' ? run.iteration : index + 1,
    timestamp: run.timestamp ?? nowIso,
    status: toCICDStatus(run.status),
    failures_remaining:
      typeof run.failures_remaining === 'number' ? run.failures_remaining : 0,
  }));

  const finalStatus = raw.final_status?.toUpperCase() === 'PASSED' ? 'PASSED' : 'FAILED';

  return {
    run_id: raw.run_id ?? `run-${Date.now()}`,
    repo_url: raw.repo_url ?? '',
    team_name: raw.team_name ?? '',
    leader_name: raw.leader_name ?? '',
    branch: raw.branch ?? raw.branch_name ?? '',
    start_time: raw.start_time ?? nowIso,
    end_time: raw.end_time ?? nowIso,
    duration_seconds: durationSeconds,
    total_failures: raw.total_failures ?? 0,
    total_fixes: totalFixes,
    total_commits: raw.total_commits ?? totalFixes,
    final_status: finalStatus,
    score: {
      base: score.base ?? 100,
      speed_bonus: score.speed_bonus ?? 0,
      penalty: score.penalty ?? 0,
      total: score.total ?? score.final_score ?? 0,
    },
    fixes: normalizedFixes,
    cicd_runs: normalizedRuns,
  };
}

export async function POST(request: NextRequest) {
  try {
    const backendUrl = process.env.AGENT_BACKEND_URL;
    if (!backendUrl) {
      return NextResponse.json(
        { message: 'AGENT_BACKEND_URL is not configured' },
        { status: 500 }
      );
    }

    const body = await request.json();
    const payload = {
      repo_url: body.repoUrl,
      team_name: body.teamName,
      leader_name: body.leaderName,
    };

    const response = await fetch(`${backendUrl.replace(/\/$/, '')}/run-agent`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      cache: 'no-store',
    });

    const data = (await response.json()) as BackendRunResult | { detail?: string };

    if (!response.ok) {
      const detail = 'detail' in data ? data.detail : 'Backend request failed';
      return NextResponse.json({ message: detail ?? 'Backend request failed' }, { status: response.status });
    }

    return NextResponse.json(normalizeResults(data as BackendRunResult));
  } catch {
    return NextResponse.json({ message: 'Unable to connect to backend' }, { status: 500 });
  }
}
