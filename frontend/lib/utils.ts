export const contemptRiskColor = (risk: string) => {
  switch (risk) {
    case 'critical': return 'bg-red-100 text-red-800 border-red-300'
    case 'red': return 'bg-orange-100 text-orange-800 border-orange-300'
    case 'amber': return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    case 'green': return 'bg-green-100 text-green-800 border-green-300'
    default: return 'bg-gray-100 text-gray-800 border-gray-300'
  }
}

export const contemptRiskLabel = (risk: string) => {
  switch (risk) {
    case 'critical': return '🔴 CRITICAL — Contempt Risk'
    case 'red': return '🟠 HIGH RISK'
    case 'amber': return '🟡 MODERATE RISK'
    case 'green': return '🟢 ON TRACK'
    default: return risk
  }
}

export const statusColor = (status: string) => {
  switch (status) {
    case 'complied': case 'verified': return 'bg-green-100 text-green-800'
    case 'in_progress': case 'assigned': return 'bg-blue-100 text-blue-800'
    case 'escalated': case 'overdue': return 'bg-red-100 text-red-800'
    case 'approved': return 'bg-purple-100 text-purple-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

export const formatDate = (dateStr: string | null) => {
  if (!dateStr) return 'Not specified'
  try {
    return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
  } catch { return dateStr }
}

export const confidenceColor = (score: number) => {
  if (score >= 0.85) return 'text-green-600 bg-green-50'
  if (score >= 0.65) return 'text-yellow-600 bg-yellow-50'
  return 'text-red-600 bg-red-50'
}

export const confidenceLabel = (score: number) => `${Math.round(score * 100)}%`

export const truncate = (str: string, n: number) => str.length > n ? str.slice(0, n) + '...' : str
