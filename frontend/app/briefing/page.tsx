'use client'
import { useEffect, useState } from 'react'
import { getBriefing } from '../../lib/api'
import ContemptTimer from '../../components/ContemptTimer'
import { formatDate, statusColor } from '../../lib/utils'
import Link from 'next/link'

export default function BriefingPage() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getBriefing().then(r => setData(r.data)).finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full" />
    </div>
  )

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      {/* Hero */}
      <div className="bg-gradient-to-r from-orange-500 to-amber-500 rounded-2xl p-6 mb-8 text-white">
        <div className="text-sm opacity-80 mb-1">Welcome back,</div>
        <h1 className="text-2xl font-bold mb-1">{data?.officer_name}</h1>
        <div className="text-sm opacity-90">{data?.department} · {data?.role}</div>
        <div className="mt-4 inline-flex items-center gap-2 bg-white/20 rounded-lg px-3 py-1.5 text-sm font-medium">
          📋 {data?.inherited_count} pending compliance obligations inherited
        </div>
      </div>

      {/* Transfer gap callout */}
      {data?.inherited_count > 0 && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-xl mb-6">
          <p className="text-sm text-red-800 font-medium">
            ⚠️ These {data.inherited_count} obligations were active before your posting. Court deadlines do not pause for transfers.
            The law holds <strong>you</strong> responsible from your first day in this role.
          </p>
        </div>
      )}

      {/* Actions */}
      <h2 className="text-lg font-semibold text-slate-800 mb-4">Your Compliance Obligations — sorted by urgency</h2>

      {(!data?.actions || data.actions.length === 0) ? (
        <div className="text-center py-12 text-slate-400 bg-white rounded-xl border border-slate-200">
          <p className="text-lg">✅ No pending obligations.</p>
          <p className="text-sm mt-1">You are fully compliant. Well done.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {data.actions.map((action: any, i: number) => (
            <Link key={action.id} href={`/verify/${action.judgment_id}`}>
              <div className={`bg-white border rounded-xl p-4 hover:shadow-md transition-shadow cursor-pointer ${
                action.contempt_risk === 'critical' ? 'border-red-300 bg-red-50' :
                action.contempt_risk === 'red' ? 'border-orange-200' :
                action.contempt_risk === 'amber' ? 'border-yellow-200' : 'border-slate-200'
              }`}>
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-slate-400 text-sm font-bold">#{i + 1}</span>
                      <ContemptTimer daysLeft={action.days_left} dueDate={action.due_date} risk={action.contempt_risk} />
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${statusColor(action.status)}`}>
                        {action.status.replace('_', ' ')}
                      </span>
                    </div>
                    <p className="text-sm text-slate-800 leading-relaxed mb-2">{action.directive_text}</p>
                    <div className="text-xs text-slate-500">
                      <span className="font-medium">{action.responsible_designation}</span>
                      {action.due_date && <> · Due: {formatDate(action.due_date)}</>}
                    </div>
                  </div>
                  <span className="text-slate-400 text-sm">→</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
