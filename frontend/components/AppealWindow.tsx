import { formatDate } from '../lib/utils'
import type { AppealWindow as AppealWindowType } from '../types/action'

interface Props { windows: AppealWindowType[] }

const appealLabels: Record<string, string> = {
  writ_appeal: 'Writ Appeal',
  slp: 'Special Leave Petition (SLP)',
  lp_appeal: 'Letters Patent Appeal',
}

export default function AppealWindow({ windows }: Props) {
  if (!windows?.length) return null
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
      <h4 className="text-sm font-semibold text-blue-800 mb-3">⚖️ Appeal Windows (Limitation Act)</h4>
      <div className="space-y-2">
        {windows.map(w => (
          <div key={w.appeal_type} className={`flex justify-between items-center text-xs p-2 rounded-lg ${
            (w.days_remaining ?? 999) <= 10 ? 'bg-red-100 border border-red-200' : 'bg-white border border-blue-100'
          }`}>
            <div>
              <div className="font-medium text-slate-800">{appealLabels[w.appeal_type] || w.appeal_type}</div>
              <div className="text-slate-500">{w.legal_basis}</div>
            </div>
            <div className="text-right">
              <div className="font-bold text-slate-700">{w.window_days} days window</div>
              <div className={`font-medium ${(w.days_remaining ?? 999) <= 10 ? 'text-red-600' : 'text-slate-600'}`}>
                {w.days_remaining !== null ? `${w.days_remaining} days left` : 'Expired'}
              </div>
              <div className="text-slate-400">{formatDate(w.deadline_date)}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
