'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { login, listDemoUsers } from '../../lib/api'

const DEMO_USERS = [
  { email: 'reviewer@karnataka.gov', role: 'reviewer', name: 'Priya Sharma', desc: 'Uploads & verifies extracted fields' },
  { email: 'officer@karnataka.gov', role: 'officer', name: 'Ravi Kumar', desc: 'Revenue Dept — sees his pending actions' },
  { email: 'new_officer@karnataka.gov', role: 'officer', name: 'Amit Patel (New Transfer)', desc: 'Urban Dev — inherits previous officer\'s obligations' },
  { email: 'head@karnataka.gov', role: 'head', name: 'Suresh Nair', desc: 'Dept Head — sees full department view' },
  { email: 'secretary@karnataka.gov', role: 'secretary', name: 'IAS Meena Iyer', desc: 'Chief Secretary — state-wide leaderboard' },
]

export default function LoginPage() {
  const [loading, setLoading] = useState<string | null>(null)
  const router = useRouter()

  const handleLogin = async (email: string) => {
    setLoading(email)
    try {
      const res = await login(email)
      localStorage.setItem('nyaaysetu_token', res.data.access_token)
      localStorage.setItem('nyaaysetu_user', JSON.stringify(res.data.user))

      // Redirect based on role
      const role = res.data.user.role
      if (role === 'secretary' || role === 'admin') router.push('/dashboard')
      else router.push('/briefing')
    } catch (e) {
      alert('Login failed')
    } finally {
      setLoading(null)
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-slate-900 mb-2">Select Demo User</h1>
        <p className="text-slate-500 text-sm">Each role sees a different view — designed for the AI for Bharat demo</p>
      </div>
      <div className="space-y-3">
        {DEMO_USERS.map(u => (
          <button key={u.email} onClick={() => handleLogin(u.email)}
            disabled={loading !== null}
            className="w-full bg-white border border-slate-200 rounded-xl p-4 text-left hover:border-orange-300 hover:bg-orange-50 transition-all disabled:opacity-60 group">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-slate-800 group-hover:text-orange-700">{u.name}</div>
                <div className="text-xs text-slate-500 mt-0.5">{u.email}</div>
                <div className="text-xs text-slate-600 mt-1">{u.desc}</div>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">{u.role}</span>
                {loading === u.email ? (
                  <div className="w-5 h-5 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
                ) : (
                  <span className="text-orange-500 text-sm">→</span>
                )}
              </div>
            </div>
          </button>
        ))}
      </div>
      <p className="text-center text-xs text-slate-400 mt-6">No passwords required · Demo mode · All data is sample Karnataka HC data</p>
    </div>
  )
}
