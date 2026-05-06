'use client'
import { useState, useEffect } from 'react'
import { contemptRiskColor } from '../lib/utils'

interface Props {
  daysLeft: number | null
  dueDate: string | null
  risk: string
  size?: 'sm' | 'lg'
}

export default function ContemptTimer({ daysLeft, dueDate, risk, size = 'sm' }: Props) {
  const [tick, setTick] = useState(0)

  useEffect(() => {
    if (risk === 'critical') {
      const t = setInterval(() => setTick(t => t + 1), 1000)
      return () => clearInterval(t)
    }
  }, [risk])

  const label = daysLeft === null
    ? 'Deadline unknown'
    : daysLeft < 0
    ? `${Math.abs(daysLeft)} days OVERDUE`
    : daysLeft === 0
    ? 'Due TODAY'
    : `${daysLeft} days remaining`

  const colorClass = contemptRiskColor(risk)
  const isLarge = size === 'lg'

  return (
    <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-xs font-semibold ${colorClass} ${risk === 'critical' ? 'animate-pulse' : ''}`}>
      <span className={`w-2 h-2 rounded-full ${risk === 'critical' ? 'bg-red-500' : risk === 'red' ? 'bg-orange-500' : risk === 'amber' ? 'bg-yellow-500' : 'bg-green-500'}`} />
      <span>{label}</span>
      {daysLeft !== null && daysLeft < 0 && <span className="font-bold">⚠️ CONTEMPT RISK</span>}
    </div>
  )
}
