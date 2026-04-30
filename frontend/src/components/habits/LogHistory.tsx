import type { HabitLog } from '../../types'

interface LogHistoryProps {
  logs: HabitLog[]
}

const STATUS_ICON: Record<string, string> = {
  done: '✅',
  partial: '🟡',
  not_done: '⚪',
}

const STATUS_LABEL: Record<string, string> = {
  done: 'Completado',
  partial: 'Parcial',
  not_done: 'No hecho',
}

function formatLogDate(isoDate: string): string {
  const d = new Date(isoDate)
  return d.toLocaleDateString('es-CO', {
    weekday: 'long',
    day: 'numeric',
    month: 'short',
  })
}

function weekLabel(logDate: Date, today: Date): string {
  const todayMs = today.setHours(0, 0, 0, 0)
  const logMs = new Date(logDate).setHours(0, 0, 0, 0)
  const diffDays = Math.floor((todayMs - logMs) / (24 * 60 * 60 * 1000))
  if (diffDays < 7) return 'Esta semana'
  if (diffDays < 14) return 'Semana anterior'
  const weeks = Math.floor(diffDays / 7)
  return `Hace ${weeks} semanas`
}

function groupLogsByWeek(logs: HabitLog[]): Map<string, HabitLog[]> {
  const today = new Date()
  const groups = new Map<string, HabitLog[]>()
  for (const log of logs) {
    const label = weekLabel(new Date(log.logged_at), today)
    if (!groups.has(label)) groups.set(label, [])
    groups.get(label)!.push(log)
  }
  return groups
}

export default function LogHistory({ logs }: LogHistoryProps) {
  const MAX_LOGS = 30
  const visible = logs.slice(0, MAX_LOGS)

  if (visible.length === 0) {
    return (
      <div className="text-center py-8 text-gray-400 text-sm">
        No hay registros aún. ¡Haz tu primer check-in!
      </div>
    )
  }

  const grouped = groupLogsByWeek(visible)

  return (
    <div className="space-y-4">
      {Array.from(grouped.entries()).map(([week, weekLogs]) => (
        <div key={week}>
          <p className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">
            {week}
          </p>
          <div className="space-y-1">
            {weekLogs.map((log) => (
              <div
                key={log.id}
                className="flex items-center gap-3 py-2 px-3 bg-white rounded-xl shadow-sm"
              >
                <span className="text-base leading-none">{STATUS_ICON[log.status]}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-800 capitalize">
                    {formatLogDate(log.logged_at)}
                  </p>
                  {log.notes && (
                    <p className="text-xs text-gray-400 truncate mt-0.5">"{log.notes}"</p>
                  )}
                </div>
                <span className="text-xs text-gray-400 shrink-0">{STATUS_LABEL[log.status]}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
      {logs.length > MAX_LOGS && (
        <p className="text-xs text-center text-gray-400 pt-1">
          Mostrando los últimos {MAX_LOGS} registros
        </p>
      )}
    </div>
  )
}
