export type ContemptRisk = 'green' | 'amber' | 'red' | 'critical'
export type ActionStatus = 'new' | 'under_review' | 'approved' | 'assigned' | 'in_progress' | 'complied' | 'verified' | 'escalated' | 'overdue'

export interface ActionItem {
  id: string
  judgment_id: string
  directive_text: string
  source_page: number
  source_bbox: string | null
  source_sentence: string | null
  action_type: string
  responsible_designation: string
  responsible_department: string
  due_date: string | null
  due_date_basis: string
  days_left: number | null
  contempt_risk: ContemptRisk
  confidence_overall: number
  confidence_directive: number
  confidence_department: number
  confidence_deadline: number
  status: ActionStatus
  is_escalated: boolean
  chain_next: string | null
  audit_logs?: AuditLog[]
}

export interface AuditLog {
  id: string
  officer_email: string
  officer_name: string | null
  event_type: string
  old_value: string | null
  new_value: string | null
  notes: string | null
  created_at: string
}

export interface AppealWindow {
  appeal_type: string
  window_days: number
  deadline_date: string | null
  days_remaining: number | null
  legal_basis: string
}

export interface Judgment {
  id: string
  case_number: string | null
  order_date: string | null
  pdf_filename: string | null
  pdf_url: string | null
  processing_status: string
  total_pages: number
  has_kannada: string
  action_items: ActionItem[]
  appeal_windows: AppealWindow[]
}

export interface LeaderboardEntry {
  department: string
  compliance_score: number
  total_actions: number
  complied_actions: number
  overdue_actions: number
  critical_actions: number
  trend: string
}

export interface DashboardSummary {
  total_actions: number
  overdue_actions: number
  critical_actions: number
  complied_actions: number
  leaderboard: LeaderboardEntry[]
}
