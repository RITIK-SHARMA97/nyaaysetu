'use client'
import { useState, useEffect } from 'react'
import { getJudgmentStatus, getJudgment } from '../lib/api'
import type { Judgment } from '../types/action'

export function useJudgment(id: string | null) {
  const [status, setStatus] = useState('pending')
  const [progress, setProgress] = useState(0)
  const [data, setData] = useState<Judgment | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    let interval: NodeJS.Timeout

    const poll = async () => {
      try {
        const res = await getJudgmentStatus(id)
        setStatus(res.data.status)
        setProgress(res.data.progress || 0)

        if (res.data.status === 'ready') {
          clearInterval(interval)
          const full = await getJudgment(id)
          setData(full.data)
        } else if (res.data.status === 'failed') {
          clearInterval(interval)
          setError(res.data.message || 'Processing failed')
        }
      } catch (e) {
        clearInterval(interval)
        setError('Connection error')
      }
    }

    poll()
    interval = setInterval(poll, 2000)
    return () => clearInterval(interval)
  }, [id])

  return { status, progress, data, error }
}
