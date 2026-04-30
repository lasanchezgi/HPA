import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import type { HabitSummary, LogCompletionResponse } from '../../types'
import LoadingSpinner from '../ui/LoadingSpinner'

interface HabitCardProps {
  habit: HabitSummary
  onCheckin: (habitId: string) => Promise<LogCompletionResponse>
  isCheckedInToday: boolean
}

function formatLastLogged(date: string | null): string {
  if (!date) return 'Never logged'

  const logged = new Date(date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const loggedDay = new Date(logged)
  loggedDay.setHours(0, 0, 0, 0)

  const diffMs = today.getTime() - loggedDay.getTime()
  const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Último: hoy'
  if (diffDays === 1) return 'Último: ayer'
  return `Último: hace ${diffDays} días`
}

type CheckinState = 'idle' | 'loading' | 'done' | 'error'

export default function HabitCard({ habit, onCheckin, isCheckedInToday }: HabitCardProps) {
  const navigate = useNavigate()
  const [state, setState] = useState<CheckinState>(isCheckedInToday ? 'done' : 'idle')
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const [newStreak, setNewStreak] = useState<number | null>(null)

  const handleCheckin = async () => {
    if (state === 'done' || state === 'loading') return

    setState('loading')
    setErrorMsg(null)

    try {
      const result = await onCheckin(habit.habit_id)
      setNewStreak(result.current_streak)
      setState('done')
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Error'
      if (msg === 'Ya registraste este hábito hoy') {
        setState('done')
      } else {
        setErrorMsg(msg)
        setState('error')
        setTimeout(() => setState('idle'), 2500)
      }
    }
  }

  return (
    <div className="bg-white rounded-2xl px-4 py-3 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <div
          className="flex-1 min-w-0 cursor-pointer"
          onClick={() => navigate(`/habits/${habit.habit_id}`)}
        >
          <p className="text-sm font-semibold text-gray-900 truncate">{habit.habit_name}</p>
          <div className="flex items-center gap-2 mt-0.5">
            <p className="text-xs text-gray-400">{formatLastLogged(habit.last_logged)}</p>
            {(newStreak ?? habit.current_streak) > 0 && (
              <span className="text-xs text-orange-500 font-semibold flex items-center gap-0.5">
                🔥 {newStreak ?? habit.current_streak}
              </span>
            )}
          </div>
          {errorMsg && (
            <p className="text-xs text-red-500 mt-1">{errorMsg}</p>
          )}
        </div>

        <button
          onClick={(e) => { e.stopPropagation(); handleCheckin() }}
          disabled={state === 'done' || state === 'loading'}
          className={`
            w-10 h-10 rounded-full flex items-center justify-center shrink-0
            border-2 transition-all duration-200
            ${state === 'done'
              ? 'bg-green-500 border-green-500 text-white cursor-default'
              : state === 'loading'
              ? 'border-blue-300 text-blue-300'
              : state === 'error'
              ? 'border-red-400 text-red-400'
              : 'border-blue-500 text-blue-500 hover:bg-blue-50 active:scale-95'
            }
          `}
        >
          {state === 'loading' ? (
            <LoadingSpinner size="sm" />
          ) : (
            <svg
              viewBox="0 0 24 24"
              className="w-5 h-5"
              fill={state === 'done' ? 'currentColor' : 'none'}
              stroke="currentColor"
              strokeWidth={state === 'done' ? 0 : 2.5}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M4.5 12.75l6 6 9-13.5"
              />
            </svg>
          )}
        </button>
      </div>
    </div>
  )
}
