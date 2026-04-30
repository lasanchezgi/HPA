import { useState, useEffect, useCallback } from 'react'
import { getHabitDetail, getHabitLogs } from '../api/habits'
import { buildConsistencyData, calculateOverallRate } from '../utils/consistency'
import type { HabitDetail, HabitLog, ConsistencyDataPoint } from '../types'

interface UseHabitDetailReturn {
  habit: HabitDetail | null
  logs: HabitLog[]
  consistencyData: ConsistencyDataPoint[]
  overallRate: number
  isLoading: boolean
  error: string | null
  refresh: () => void
}

export const useHabitDetail = (habitId: string): UseHabitDetailReturn => {
  const [habit, setHabit] = useState<HabitDetail | null>(null)
  const [logs, setLogs] = useState<HabitLog[]>([])
  const [consistencyData, setConsistencyData] = useState<ConsistencyDataPoint[]>([])
  const [overallRate, setOverallRate] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const [habitData, logsData] = await Promise.all([
        getHabitDetail(habitId),
        getHabitLogs(habitId),
      ])
      const data = buildConsistencyData(logsData, habitData.habit_start_date, habitData.frequency_code)
      setHabit(habitData)
      setLogs(logsData)
      setConsistencyData(data)
      setOverallRate(calculateOverallRate(data))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error cargando el hábito')
    } finally {
      setIsLoading(false)
    }
  }, [habitId])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  return { habit, logs, consistencyData, overallRate, isLoading, error, refresh: fetchData }
}
