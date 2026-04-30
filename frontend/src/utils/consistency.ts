import type { HabitLog, ConsistencyDataPoint } from '../types'

const WEEK_MS = 7 * 24 * 60 * 60 * 1000

function startOfDayUTC(d: Date): Date {
  return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()))
}

function weekStart(d: Date): Date {
  const day = startOfDayUTC(d)
  const dow = day.getUTCDay()
  // Monday as week start
  const diff = (dow === 0 ? -6 : 1 - dow)
  return new Date(day.getTime() + diff * 24 * 60 * 60 * 1000)
}

function totalPerWeek(frequencyCode: string): number {
  switch (frequencyCode.toLowerCase()) {
    case 'weekly': return 1
    case 'monthly': return 1
    default: return 7  // daily
  }
}

export const buildConsistencyData = (
  logs: HabitLog[],
  habitStartDate: string,
  frequencyCode: string,
): ConsistencyDataPoint[] => {
  const today = startOfDayUTC(new Date())
  const start = startOfDayUTC(new Date(habitStartDate))
  const habitWeekStart = weekStart(start)

  const msFromStart = today.getTime() - habitWeekStart.getTime()
  const totalWeeks = Math.min(Math.ceil(msFromStart / WEEK_MS) + 1, 12)
  const numWeeks = Math.max(totalWeeks, 8)

  // Build a set of week-start timestamps → completed count
  const completedByWeek = new Map<number, number>()
  for (const log of logs) {
    if (log.status === 'done' || log.status === 'partial') {
      const logDate = new Date(log.logged_at)
      const ws = weekStart(logDate).getTime()
      completedByWeek.set(ws, (completedByWeek.get(ws) ?? 0) + 1)
    }
  }

  const expectedTotal = totalPerWeek(frequencyCode)
  const result: ConsistencyDataPoint[] = []

  // Most recent week last → iterate from oldest to newest
  const latestWeekStart = weekStart(today)
  for (let i = numWeeks - 1; i >= 0; i--) {
    const ws = new Date(latestWeekStart.getTime() - i * WEEK_MS)
    const completed = completedByWeek.get(ws.getTime()) ?? 0
    const rate = Math.min(Math.round((completed / expectedTotal) * 100), 100)
    result.push({
      week: `Sem ${numWeeks - i}`,
      completed,
      total: expectedTotal,
      rate,
    })
  }

  return result
}

export const calculateOverallRate = (data: ConsistencyDataPoint[]): number => {
  const relevant = data.filter(d => d.total > 0)
  if (relevant.length === 0) return 0
  return Math.round(relevant.reduce((sum, d) => sum + d.rate, 0) / relevant.length)
}

export const consistencyLabel = (rate: number): string => {
  if (rate >= 80) return 'Master'
  if (rate >= 60) return 'Consistent'
  if (rate >= 30) return 'Building'
  return 'Beginner'
}
