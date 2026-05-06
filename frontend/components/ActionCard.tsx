'use client'
import { useState } from 'react'
import { contemptRiskColor, contemptRiskLabel, statusColor, formatDate } from '../lib/utils'
import { patchActionStatus, getAffidavit } from '../lib/api'
import ContemptTimer from './ContemptTimer'
import AuditLog from './AuditLog'
import AffidavitGenerator from './AffidavitGenerator'
import type { ActionItem } from '../types/action'

interface Props { action: ActionItem; onUpdated: () => void }

const NEXT_STATUS: Record<string, string[]> = {
  new: ['under_review', 'approved'],
  under_review: ['approved'],
  approved: ['assigned', 'in_progress'],
  assigned: ['in_progress'],
  in_progress: ['complied'],
  complied: ['verified'],
  escalated: ['in_progress', 'complied'],
  overdue: ['in_progress', 'complied'],
}

export default function ActionCard({ action, onUpdated }: Props) {
  const [expanded, setExpanded] = useState(false)
  const [showAudit, setShowAudit] = useState(false)
  const [showAffidavit, setShowAffidavit] = useState(false)
  const [affidavitText, setAffidavitText] = useState('')
  const [updating, setUpdating] = useState(false)
  const [localStatus, setLocalStatus] = useState(action.status)

  const nextStatuses = NEXT_STATUS[localStatus] || []

  const updateStatus = async (status: string) => {
    setUpdating(true)
    try {
      await patchActionStatus(action.id, status)
      setLocalStatus(status as any)
      onUpdated()
    } finally {
      setUpdating(false)
    }
  }

  const fetchAffidavit = async () => {
    const res = await getAffidavit(action.id)
    setAffidavitText(res.data.affidavit_text)
    setShowAffidavit(true)
  }

  return (
    <div className={`bg-white border rounded-xl mb-4 overflow-hidden shadow-sm ${
      action.contempt_risk === 'critical' ? 'border-red-300' :
      action.contempt_risk === 'red' ? 'border-orange-300' :
      action.contempt_risk === 'amber' ? 'border-yellow-300' : 'border-slate-200'
    }`}>
      <div className="p-4">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex gap-2 flex-wrap">
            <ContemptTimer daysLeft={action.days_left} dueDate={action.due_date} risk={action.contempt_risk} />
            {action.is_escalated && (
              <span className="text-xs px-2 py-0.5 rounded-full bg-red-100 text-red-700 font-medium border border-red-200">⚠️ Escalated</span>
            )}
          </div>
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${statusColor(localStatus)}`}>
            {localStatus.replace('_', ' ')}
          </span>
        </div>

        <p className="text-sm text-slate-800 leading-relaxed mb-3 font-medium">{action.directive_text}</p>

        <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-slate-600 mb-3">
          <div><span className="font-medium text-slate-700">Designation:</span> {action.responsible_designation}</div>
          <div><span className="font-medium text-slate-700">Department:</span> {action.responsible_department}</div>
          <div><span className="font-medium text-slate-700">Due Date:</span> {formatDate(action.due_date)}</div>
          <div><span className="font-medium text-slate-700">Type:</span> {action.action_type}</div>
        </div>

        {/* Action buttons */}
        <div className="flex gap-2 flex-wrap">
          {nextStatuses.map(s => (
            <button key={s} onClick={() => updateStatus(s)} disabled={updating}
              className="text-xs bg-blue-500 text-white px-3 py-1.5 rounded-lg hover:bg-blue-600 disabled:opacity-50 font-medium">
              Mark: {s.replace('_', ' ')}
            </button>
          ))}
          {(localStatus === 'complied' || localStatus === 'verified') && (
            <button onClick={fetchAffidavit}
              className="text-xs bg-green-500 text-white px-3 py-1.5 rounded-lg hover:bg-green-600 font-medium">
              📄 Generate Affidavit
            </button>
          )}
          <button onClick={() => setShowAudit(!showAudit)}
            className="text-xs bg-slate-100 text-slate-600 px-3 py-1.5 rounded-lg hover:bg-slate-200">
            📋 Audit Trail
          </button>
          <button onClick={() => setExpanded(!expanded)}
            className="text-xs bg-slate-100 text-slate-600 px-3 py-1.5 rounded-lg hover:bg-slate-200">
            {expanded ? '▲ Less' : '▼ Details'}
          </button>
        </div>

        {expanded && (
          <div className="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600 space-y-1">
            <div><span className="font-medium">Deadline basis:</span> {action.due_date_basis}</div>
            <div><span className="font-medium">Source page:</span> {action.source_page}</div>
            <div><span className="font-medium">Confidence:</span> Overall {Math.round(action.confidence_overall * 100)}% · Directive {Math.round(action.confidence_directive * 100)}% · Dept {Math.round(action.confidence_department * 100)}% · Deadline {Math.round(action.confidence_deadline * 100)}%</div>
            {action.source_sentence && (
              <div className="mt-2 p-2 bg-yellow-50 border border-yellow-200 rounded-lg italic">
                <span className="font-medium not-italic">Source: </span>{action.source_sentence}
              </div>
            )}
          </div>
        )}
      </div>

      {showAudit && action.audit_logs && (
        <div className="border-t border-slate-100"><AuditLog logs={action.audit_logs} /></div>
      )}
      {showAffidavit && (
        <div className="border-t border-slate-100">
          <AffidavitGenerator text={affidavitText} onClose={() => setShowAffidavit(false)} />
        </div>
      )}
    </div>
  )
}
