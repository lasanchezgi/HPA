import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useHabitDetail } from '../hooks/useHabitDetail'
import { archiveHabit } from '../api/habits'
import ConsistencyChart from '../components/habits/ConsistencyChart'
import LogHistory from '../components/habits/LogHistory'
import EditHabitModal from '../components/habits/EditHabitModal'

const CATEGORY_EMOJI: Record<string, string> = {
  health: '🏃',
  salud: '🏃',
  productivity: '⚡',
  productividad: '⚡',
  learning: '📚',
  aprendizaje: '📚',
  mindfulness: '🧘',
  fitness: '💪',
  nutrition: '🥗',
  social: '👥',
}

function categoryEmoji(code: string): string {
  return CATEGORY_EMOJI[code.toLowerCase()] ?? '✨'
}

function frequencyLabel(code: string): string {
  const map: Record<string, string> = {
    daily: 'Diario',
    diario: 'Diario',
    weekly: 'Semanal',
    semanal: 'Semanal',
    monthly: 'Mensual',
    mensual: 'Mensual',
  }
  return map[code.toLowerCase()] ?? code
}

function Skeleton({ className }: { className: string }) {
  return <div className={`animate-pulse bg-gray-200 rounded-xl ${className}`} />
}

export default function HabitDetailPage() {
  const { habitId } = useParams<{ habitId: string }>()
  const navigate = useNavigate()
  const { habit, logs, consistencyData, overallRate, isLoading, error, refresh } =
    useHabitDetail(habitId!)

  const [menuOpen, setMenuOpen] = useState(false)
  const [archiving, setArchiving] = useState(false)
  const [confirmArchive, setConfirmArchive] = useState(false)
  const [editModalOpen, setEditModalOpen] = useState(false)

  const handleArchive = async () => {
    setArchiving(true)
    try {
      await archiveHabit(habitId!)
      navigate(-1)
    } catch {
      setArchiving(false)
      setConfirmArchive(false)
    }
  }

  const daysSinceStart = habit
    ? Math.floor((Date.now() - new Date(habit.habit_start_date).getTime()) / 86400000)
    : 0

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white px-4 pt-12 pb-4 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-1 text-blue-600 text-sm font-medium"
          >
            <svg viewBox="0 0 24 24" className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Volver
          </button>

          <div className="relative">
            <button
              onClick={() => setMenuOpen(v => !v)}
              className="text-gray-400 p-1"
              aria-label="Opciones"
            >
              <svg viewBox="0 0 24 24" className="w-6 h-6" fill="currentColor">
                <circle cx="12" cy="5" r="1.5" />
                <circle cx="12" cy="12" r="1.5" />
                <circle cx="12" cy="19" r="1.5" />
              </svg>
            </button>
            {menuOpen && (
              <div className="absolute right-0 mt-1 w-44 bg-white rounded-xl shadow-lg border border-gray-100 z-10">
                <button
                  className="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 rounded-t-xl"
                  onClick={() => { setMenuOpen(false); setEditModalOpen(true) }}
                >
                  Editar hábito
                </button>
                <button
                  className="w-full text-left px-4 py-3 text-sm text-red-500 hover:bg-red-50 rounded-b-xl border-t border-gray-100"
                  onClick={() => { setMenuOpen(false); setConfirmArchive(true) }}
                >
                  Archivar hábito
                </button>
              </div>
            )}
          </div>
        </div>

        {isLoading ? (
          <div className="space-y-2">
            <Skeleton className="h-7 w-48" />
            <Skeleton className="h-4 w-32" />
            <Skeleton className="h-4 w-24 mt-1" />
          </div>
        ) : error ? null : habit ? (
          <>
            <div className="flex items-center gap-2">
              <span className="text-3xl">{categoryEmoji(habit.category_code)}</span>
              <div>
                <h1 className="text-xl font-bold text-gray-900">{habit.habit_name}</h1>
                {habit.habit_description && (
                  <p className="text-sm text-gray-500 mt-0.5">{habit.habit_description}</p>
                )}
                <p className="text-xs text-gray-400 mt-0.5">
                  {frequencyLabel(habit.frequency_code)} · {habit.category_code}
                </p>
              </div>
            </div>
          </>
        ) : null}
      </div>

      {error ? (
        <div className="flex flex-col items-center justify-center py-20 gap-4">
          <p className="text-gray-500 text-sm">{error}</p>
          <button
            onClick={refresh}
            className="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm font-medium"
          >
            Reintentar
          </button>
        </div>
      ) : (
        <div className="px-4 py-4 space-y-4 max-w-lg mx-auto">
          {/* Stats row */}
          {isLoading ? (
            <div className="grid grid-cols-3 gap-3">
              {[0, 1, 2].map(i => <Skeleton key={i} className="h-16" />)}
            </div>
          ) : habit ? (
            <div className="grid grid-cols-3 gap-3">
              <div className="bg-white rounded-2xl p-3 text-center shadow-sm">
                <p className="text-2xl font-bold text-orange-500">🔥 {habit.current_streak}</p>
                <p className="text-xs text-gray-400 mt-1">Racha</p>
              </div>
              <div className="bg-white rounded-2xl p-3 text-center shadow-sm">
                <p className="text-2xl font-bold text-purple-500">💎 {habit.best_streak}</p>
                <p className="text-xs text-gray-400 mt-1">Mejor racha</p>
              </div>
              <div className="bg-white rounded-2xl p-3 text-center shadow-sm">
                <p className="text-2xl font-bold text-blue-500">📅 {daysSinceStart}</p>
                <p className="text-xs text-gray-400 mt-1">Días</p>
              </div>
            </div>
          ) : null}

          {/* Consistency chart */}
          <div className="bg-white rounded-2xl p-4 shadow-sm">
            {isLoading ? (
              <Skeleton className="h-48" />
            ) : (
              <ConsistencyChart data={consistencyData} overallRate={overallRate} />
            )}
          </div>

          {/* Log history */}
          <div className="bg-transparent">
            <p className="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-3">
              Historial
            </p>
            {isLoading ? (
              <div className="space-y-2">
                {[0, 1, 2].map(i => <Skeleton key={i} className="h-12" />)}
              </div>
            ) : (
              <LogHistory logs={logs} />
            )}
          </div>
        </div>
      )}

      {/* Archive confirmation modal */}
      {confirmArchive && (
        <div className="fixed inset-0 bg-black/40 flex items-end justify-center z-20 pb-8 px-4">
          <div className="bg-white rounded-2xl p-6 w-full max-w-sm shadow-xl">
            <h3 className="font-semibold text-gray-900 mb-2">¿Archivar este hábito?</h3>
            <p className="text-sm text-gray-500 mb-5">
              No aparecerá en tu dashboard. Puedes recuperarlo más tarde.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setConfirmArchive(false)}
                disabled={archiving}
                className="flex-1 py-2.5 rounded-xl border border-gray-200 text-sm font-medium text-gray-600"
              >
                Cancelar
              </button>
              <button
                onClick={handleArchive}
                disabled={archiving}
                className="flex-1 py-2.5 rounded-xl bg-red-500 text-white text-sm font-medium disabled:opacity-60"
              >
                {archiving ? 'Archivando…' : 'Archivar'}
              </button>
            </div>
          </div>
        </div>
      )}

      {menuOpen && (
        <div className="fixed inset-0 z-0" onClick={() => setMenuOpen(false)} />
      )}

      {habit && (
        <EditHabitModal
          isOpen={editModalOpen}
          habit={habit}
          onClose={() => setEditModalOpen(false)}
          onHabitUpdated={() => {
            refresh()
            setEditModalOpen(false)
          }}
        />
      )}
    </div>
  )
}
