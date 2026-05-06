import type { AuditLog as AuditLogType } from '../types/action'

interface Props { logs: AuditLogType[] }

const eventIcon: Record<string, string> = {
  approve: '✅', edit: '✏️', reject: '❌', status_changed: '🔄', escalated: '⚠️'
}

export default function AuditLog({ logs }: Props) {
  if (!logs?.length) return (
    <div className="p-4 text-sm text-slate-500 text-center">No audit entries yet</div>
  )
  return (
    <div className="p-4">
      <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">Audit Trail — Immutable</h4>
      <div className="space-y-2">
        {logs.map(log => (
          <div key={log.id} className="flex gap-3 text-xs">
            <span className="text-base">{eventIcon[log.event_type] || '📝'}</span>
            <div className="flex-1">
              <span className="font-medium text-slate-800">{log.officer_name || log.officer_email}</span>
              <span className="text-slate-500"> · {log.event_type.replace('_', ' ')}</span>
              {log.new_value && log.event_type === 'status_changed' && (
                <span className="text-slate-500"> → <span className="font-medium text-blue-600">{log.new_value}</span></span>
              )}
              <div className="text-slate-400">{log.created_at ? new Date(log.created_at).toLocaleString('en-IN') : ''}</div>
              {log.notes && <div className="text-slate-600 italic">{log.notes}</div>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
