import type { LeaderboardEntry } from '../types/action'

interface Props { entries: LeaderboardEntry[] }

const trendIcon = (t: string) => t === 'improving' ? '📈' : t === 'worsening' ? '📉' : '➡️'

export default function Leaderboard({ entries }: Props) {
  if (!entries?.length) return (
    <div className="text-center py-8 text-slate-500 text-sm">No data yet. Upload judgments to see department rankings.</div>
  )
  return (
    <div>
      <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Department Compliance Leaderboard</h3>
      <div className="space-y-3">
        {entries.map((e, i) => (
          <div key={e.department} className={`flex items-center gap-4 p-3 rounded-xl border ${
            i === 0 ? 'bg-green-50 border-green-200' :
            entries.length - 1 === i ? 'bg-red-50 border-red-200' : 'bg-white border-slate-200'
          }`}>
            <span className="text-xl font-bold text-slate-400 w-6">#{i + 1}</span>
            <div className="flex-1 min-w-0">
              <div className="font-medium text-slate-800 text-sm truncate">{e.department}</div>
              <div className="flex gap-3 text-xs text-slate-500 mt-0.5">
                <span>{e.total_actions} actions</span>
                <span className="text-green-600">{e.complied_actions} complied</span>
                {e.overdue_actions > 0 && <span className="text-red-600">{e.overdue_actions} overdue</span>}
                {e.critical_actions > 0 && <span className="text-red-700 font-medium">{e.critical_actions} critical</span>}
              </div>
            </div>
            <div className="text-right">
              <div className={`text-xl font-bold ${
                e.compliance_score >= 80 ? 'text-green-600' :
                e.compliance_score >= 50 ? 'text-yellow-600' : 'text-red-600'
              }`}>{e.compliance_score}%</div>
              <div className="text-xs text-slate-500">{trendIcon(e.trend)} {e.trend}</div>
            </div>
            <div className="w-16">
              <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                <div className={`h-full rounded-full ${
                  e.compliance_score >= 80 ? 'bg-green-500' :
                  e.compliance_score >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                }`} style={{ width: `${e.compliance_score}%` }} />
              </div>
            </div>
          </div>
        ))}
      </div>
      <p className="text-xs text-slate-400 mt-4 text-center italic">
        "Until NyaaySetu, nobody could answer which Karnataka department worst complied with court orders."
      </p>
    </div>
  )
}
