'use client'
import { useState } from 'react'
import { confidenceColor, confidenceLabel, formatDate } from '../lib/utils'
import { patchAction } from '../lib/api'
import ContemptTimer from './ContemptTimer'
import type { ActionItem } from '../types/action'

interface Props {
  action: ActionItem
  onFieldClick: (action: ActionItem) => void
  onUpdated: () => void
  isSelected: boolean
}

export default function FieldReview({ action, onFieldClick, onUpdated, isSelected }: Props) {
  const [editing, setEditing] = useState(false)
  const [editText, setEditText] = useState(action.directive_text)
  const [loading, setLoading] = useState(false)
  const [localStatus, setLocalStatus] = useState(action.status)

  const handleDecision = async (decision: 'approve' | 'edit' | 'reject') => {
    setLoading(true)
    try {
      await patchAction(action.id, {
        decision,
        edited_value: decision === 'edit' ? editText : undefined,
      })
      setLocalStatus(decision === 'reject' ? 'new' : 'approved')
      setEditing(false)
      onUpdated()
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      className={`border rounded-xl p-4 mb-3 cursor-pointer transition-all ${
        isSelected ? 'border-orange-400 bg-orange-50 shadow-md' : 'border-slate-200 bg-white hover:border-slate-300'
      }`}
      onClick={() => onFieldClick(action)}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex gap-2 flex-wrap">
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${confidenceColor(action.confidence_overall)}`}>
            AI Confidence: {confidenceLabel(action.confidence_overall)}
          </span>
          {action.is_escalated && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-red-100 text-red-700 font-medium">⚠️ Escalated</span>
          )}
        </div>
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
          localStatus === 'approved' ? 'bg-green-100 text-green-700' :
          localStatus === 'new' ? 'bg-gray-100 text-gray-600' : 'bg-blue-100 text-blue-700'
        }`}>{localStatus}</span>
      </div>

      {editing ? (
        <textarea
          className="w-full text-sm border border-slate-300 rounded-lg p-2 mb-2 resize-none focus:outline-none focus:ring-2 focus:ring-orange-300"
          rows={3}
          value={editText}
          onChange={e => setEditText(e.target.value)}
          onClick={e => e.stopPropagation()}
        />
      ) : (
        <p className="text-sm text-slate-800 mb-2 leading-relaxed">{action.directive_text}</p>
      )}

      <div className="grid grid-cols-2 gap-2 mb-3 text-xs text-slate-600">
        <div><span className="font-medium">Designation:</span> {action.responsible_designation}</div>
        <div><span className="font-medium">Dept:</span> {action.responsible_department}</div>
        <div><span className="font-medium">Due:</span> {formatDate(action.due_date)}</div>
        <div><span className="font-medium">Type:</span> {action.action_type}</div>
      </div>

      <ContemptTimer daysLeft={action.days_left} dueDate={action.due_date} risk={action.contempt_risk} />

      {localStatus !== 'approved' && (
        <div className="flex gap-2 mt-3" onClick={e => e.stopPropagation()}>
          <button
            className="flex-1 text-xs bg-green-500 text-white rounded-lg py-1.5 font-medium hover:bg-green-600 disabled:opacity-50"
            onClick={() => handleDecision('approve')}
            disabled={loading}
          >✓ Approve</button>
          <button
            className="flex-1 text-xs bg-blue-500 text-white rounded-lg py-1.5 font-medium hover:bg-blue-600"
            onClick={() => { setEditing(!editing) }}
          >✏️ Edit</button>
          {editing && (
            <button
              className="flex-1 text-xs bg-orange-500 text-white rounded-lg py-1.5 font-medium hover:bg-orange-600 disabled:opacity-50"
              onClick={() => handleDecision('edit')}
              disabled={loading}
            >Save</button>
          )}
          <button
            className="flex-1 text-xs bg-red-100 text-red-700 rounded-lg py-1.5 font-medium hover:bg-red-200 disabled:opacity-50"
            onClick={() => handleDecision('reject')}
            disabled={loading}
          >✗ Reject</button>
        </div>
      )}
      {localStatus === 'approved' && (
        <p className="mt-2 text-xs text-green-600 font-medium">✅ Verified and approved</p>
      )}
    </div>
  )
}
