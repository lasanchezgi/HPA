import { useState, useEffect } from 'react'
import { getDashboard } from '../api/habits'
import type { DashboardSummary } from '../types'

export function useHabits() {
  const [data, setData] = useState<DashboardSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    const fetch = async () => {
      try {
        setLoading(true)
        setError(null)
        const result = await getDashboard()
        if (!cancelled) setData(result)
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Error inesperado')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    fetch()
    return () => { cancelled = true }
  }, [])

  return { data, loading, error }
}
