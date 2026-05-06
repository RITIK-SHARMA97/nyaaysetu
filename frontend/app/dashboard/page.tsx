'use client'
import { useState, useEffect } from 'react'
import { getDashboard, getDashboardActions } from '../../lib/api'
import ActionCard from '../../components/ActionCard'
import Leaderboard from '../../components/Leaderboard'
import type { DashboardSummary, ActionItem } from '../../types/action'

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [actions, setActions] = useState<ActionItem[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<string>('')
  const [riskFilter, setRiskFilter] = useState<string>('')
  const [activeTab, setActiveTab] = useState<'actions' | 'leaderboard'>('actions')

  const load = async () => {
    try {
      const [sumRes, actRes] = await Promise.all([getDashboard(), getDashboardActions(1, filter||undefined, riskFilter||undefined)])
      setSummary(sumRes.data)
      setActions(actRes.data.items || [])
    } catch (e) { console.error(e) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [filter, riskFilter])

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full" />
    </div>
  )

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Compliance Dashboard</h1>
          <p className="text-sm text-slate-500">Karnataka Government · Court Order Compliance</p>
        </div>
        <a href="/" className="text-sm bg-orange-500 text-white px-3 py-2 rounded-lg hover:bg-orange-600">
          + Upload Judgment
        </a>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Total Actions', val: summary?.total_actions || 0, color: 'blue' },
          { label: 'Overdue', val: summary?.overdue_actions || 0, color: 'red' },
          { label: 'Critical Risk', val: summary?.critical_actions || 0, color: 'orange' },
          { label: 'Complied', val: summary?.complied_actions || 0, color: 'green' },
        ].map(card => (
          <div key={card.label} className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm text-center">
            <div className={`text-3xl font-bold ${
              card.color === 'red' ? 'text-red-600' : card.color === 'orange' ? 'text-orange-500' :
              card.color === 'green' ? 'text-green-600' : 'text-blue-600'
            }`}>{card.val}</div>
            <div className="text-sm text-slate-600 mt-1">{card.label}</div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-slate-200">
        {['actions', 'leaderboard'].map(tab => (
          <button key={tab} onClick={() => setActiveTab(tab as any)}
            className={`px-4 py-2 text-sm font-medium capitalize border-b-2 transition-colors ${
              activeTab === tab ? 'border-orange-500 text-orange-600' : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}>{tab === 'leaderboard' ? '🏆 Dept Leaderboard' : '📋 Action Items'}</button>
        ))}
      </div>

      {activeTab === 'actions' && (
        <>
          {/* Filters */}
          <div className="flex gap-3 mb-4">
            <select value={riskFilter} onChange={e => setRiskFilter(e.target.value)}
              className="text-sm border border-slate-200 rounded-lg px-3 py-1.5 bg-white">
              <option value="">All Risk Levels</option>
              <option value="critical">🔴 Critical</option>
              <option value="red">🟠 High Risk</option>
              <option value="amber">🟡 Moderate</option>
              <option value="green">🟢 On Track</option>
            </select>
            <select value={filter} onChange={e => setFilter(e.target.value)}
              className="text-sm border border-slate-200 rounded-lg px-3 py-1.5 bg-white">
              <option value="">All Statuses</option>
              <option value="new">New</option>
              <option value="in_progress">In Progress</option>
              <option value="overdue">Overdue</option>
              <option value="complied">Complied</option>
            </select>
            <button onClick={load} className="text-sm text-slate-500 hover:text-slate-700 px-2">↻ Refresh</button>
          </div>
          {actions.length === 0 ? (
            <div className="text-center py-12 text-slate-400">
              <p className="text-lg">No actions found.</p>
              <a href="/" className="text-sm text-orange-500 hover:underline mt-2 block">Upload a judgment to get started →</a>
            </div>
          ) : (
            actions.map(a => <ActionCard key={a.id} action={a} onUpdated={load} />)
          )}
        </>
      )}

      {activeTab === 'leaderboard' && (
        <Leaderboard entries={summary?.leaderboard || []} />
      )}
    </div>
  )
}
