export type BugType =
  | 'LINTING'
  | 'SYNTAX'
  | 'LOGIC'
  | 'TYPE_ERROR'
  | 'IMPORT'
  | 'INDENTATION';

export type FixStatus = 'FIXED' | 'FAILED';
export type CICDStatus = 'PASSED' | 'FAILED' | 'RUNNING';
export type RunStatus = 'idle' | 'running' | 'complete' | 'error';

export interface Fix {
  file: string;
  bug_type: BugType;
  line_number: number;
  commit_message: string;
  status: FixStatus;
}

export interface CICDRun {
  run_number: number;
  timestamp: string;
  status: CICDStatus;
  failures_remaining: number;
}

export interface ScoreBreakdown {
  base: number;
  speed_bonus: number;
  penalty: number;
  total: number;
}

export interface AgentResults {
  run_id: string;
  repo_url: string;
  team_name: string;
  leader_name: string;
  branch: string;
  start_time: string;
  end_time: string;
  duration_seconds: number;
  total_failures: number;
  total_fixes: number;
  total_commits: number;
  final_status: 'PASSED' | 'FAILED';
  score: ScoreBreakdown;
  fixes: Fix[];
  cicd_runs: CICDRun[];
}

export interface LogLine {
  time: string;
  message: string;
}
