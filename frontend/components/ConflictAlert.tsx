interface Conflict {
  new_directive: string
  existing_directive: string
  department: string
  similarity_score: number
}
interface Props { conflicts: Conflict[] }

export default function ConflictAlert({ conflicts }: Props) {
  if (!conflicts?.length) return null
  return (
    <div className="bg-orange-50 border-2 border-orange-400 rounded-xl p-4 mb-4">
      <h4 className="text-sm font-bold text-orange-800 mb-3">⚠️ CONFLICT DETECTED — Potentially Contradictory Orders</h4>
      {conflicts.map((c, i) => (
        <div key={i} className="grid grid-cols-2 gap-3 mb-3">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-xs">
            <div className="font-semibold text-blue-700 mb-1">This Judgment</div>
            <p className="text-slate-700">{c.new_directive}</p>
          </div>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-xs">
            <div className="font-semibold text-yellow-700 mb-1">Existing Order (same dept)</div>
            <p className="text-slate-700">{c.existing_directive}</p>
          </div>
          <div className="col-span-2 text-xs text-orange-700 font-medium text-center">
            Department: {c.department} · Similarity: {Math.round(c.similarity_score * 100)}% · Requires senior review
          </div>
        </div>
      ))}
    </div>
  )
}
