import { useState, useEffect, useCallback } from 'react'
import { getDashboard, getHabits } from '../api/habits'
import type { DashboardSummary, HabitSummary } from '../types'

export type HabitSummaryEx = HabitSummary & {
  category_code: string
  frequency_code: string
}

type DashboardEx = Omit<DashboardSummary, 'habits_summary'> & {
  habits_summary: HabitSummaryEx[]
}

export function useHabits() {
  const [data, setData] = useState<DashboardEx | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [refreshKey, setRefreshKey] = useState(0)

  useEffect(() => {
    let cancelled = false

    const fetch = async () => {
      try {
        setLoading(true)
        setError(null)
        const [dashboard, habits] = await Promise.all([getDashboard(), getHabits()])
        if (!cancelled) {
          const habitMap = new Map(habits.map(h => [h.id, h]))
          const mergedSummary: HabitSummaryEx[] = dashboard.habits_summary.map(s => ({
            ...s,
            category_code: habitMap.get(s.habit_id)?.category_code ?? '',
            frequency_code: habitMap.get(s.habit_id)?.frequency_code ?? '',
          }))
          setData({ ...dashboard, habits_summary: mergedSummary })
        }
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Error inesperado')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    fetch()
    return () => { cancelled = true }
  }, [refreshKey])

  const refresh = useCallback(() => {
    setRefreshKey((k) => k + 1)
  }, [])

  return { data, loading, error, refresh }
}
