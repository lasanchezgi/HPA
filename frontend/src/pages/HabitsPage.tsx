import { useState, useMemo } from 'react'
import { useHabits, type HabitSummaryEx } from '../hooks/useHabits'
import { logCompletion } from '../api/habits'
import HabitCard from '../components/habits/HabitCard'
import CreateHabitModal from '../components/habits/CreateHabitModal'
import BottomNav from '../components/layout/BottomNav'
import StreakCelebration from '../components/ui/StreakCelebration'
import type { LogCompletionResponse } from '../types'

const CATEGORIES = [
  { label: 'Todos', code: '' },
  { label: '💪 Salud', code: 'health' },
  { label: '📚 Aprendizaje', code: 'learning' },
  { label: '🧘 Mindfulness', code: 'mindfulness' },
  { label: '🏋️ Fitness', code: 'fitness' },
]

const FREQUENCIES = [
  { label: 'Todos', code: '' },
  { label: 'Diario', code: 'daily' },
  { label: 'Semanal', code: 'weekly' },
  { label: 'Días hábiles', code: 'weekdays' },
]

function SkeletonCard() {
  return (
    <div className="bg-white rounded-2xl px-4 py-3 shadow-sm animate-pulse">
      <div className="flex items-center justify-between gap-3">
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-gray-200 rounded w-3/4" />
          <div className="h-3 bg-gray-200 rounded w-1/3" />
        </div>
        <div className="w-10 h-10 rounded-full bg-gray-200 shrink-0" />
      </div>
    </div>
  )
}

const isCheckedInToday = (habit: HabitSummaryEx): boolean => {
  if (!habit.last_logged) return false
  return new Date(habit.last_logged).toDateString() === new Date().toDateString()
}

export default function HabitsPage() {
  const { data, loading, error, refresh } = useHabits()
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [celebration, setCelebration] = useState<{ visible: boolean; streak: number }>({
    visible: false,
    streak: 0,
  })

  const [search, setSearch] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [frequencyFilter, setFrequencyFilter] = useState('')

  const filteredHabits = useMemo(() => {
    if (!data) return []
    const q = search.trim().toLowerCase()
    return data.habits_summary.filter(h => {
      if (q && !h.habit_name.toLowerCase().includes(q)) return false
      if (categoryFilter && h.category_code !== categoryFilter) return false
      if (frequencyFilter && h.frequency_code !== frequencyFilter) return false
      return true
    })
  }, [data, search, categoryFilter, frequencyFilter])

  const hasActiveFilters = search.trim() !== '' || categoryFilter !== '' || frequencyFilter !== ''

  const handleCheckin = async (habitId: string): Promise<LogCompletionResponse> => {
    const result = await logCompletion(habitId, { status: 'done' })
    if (result.current_streak >= 3) {
      setCelebration({ visible: true, streak: result.current_streak })
    }
    refresh()
    return result
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="bg-white px-6 pt-12 pb-4 shadow-sm">
        <h1 className="text-xl font-bold text-gray-900 mb-4">Mis hábitos</h1>

        {/* Search bar */}
        <div className="flex items-center gap-2 bg-gray-100 rounded-xl px-3 py-2">
          <svg className="w-4 h-4 text-gray-400 shrink-0" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
          </svg>
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Buscar hábito…"
            className="flex-1 bg-transparent text-sm text-gray-900 placeholder:text-gray-400 focus:outline-none"
          />
          {search && (
            <button onClick={() => setSearch('')} className="text-gray-400 hover:text-gray-600 shrink-0">
              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          )}
        </div>

        {/* Category chips */}
        <div className="flex gap-2 mt-3 overflow-x-auto pb-1 scrollbar-none">
          {CATEGORIES.map(c => (
            <button
              key={c.code}
              onClick={() => setCategoryFilter(c.code)}
              className={`shrink-0 px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                categoryFilter === c.code
                  ? 'bg-blue-500 text-white border-blue-500'
                  : 'bg-white text-gray-600 border-gray-300'
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>

        {/* Frequency chips */}
        <div className="flex gap-2 mt-2 overflow-x-auto pb-1 scrollbar-none">
          {FREQUENCIES.map(f => (
            <button
              key={f.code}
              onClick={() => setFrequencyFilter(f.code)}
              className={`shrink-0 px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                frequencyFilter === f.code
                  ? 'bg-indigo-500 text-white border-indigo-500'
                  : 'bg-white text-gray-600 border-gray-300'
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      <div className="max-w-sm mx-auto px-6 mt-6">
        {loading && (
          <div className="flex flex-col gap-3">
            {[0, 1, 2].map((i) => <SkeletonCard key={i} />)}
          </div>
        )}

        {error && (
          <div className="flex flex-col items-center gap-3 py-12">
            <p className="text-sm text-red-500 text-center">{error}</p>
            <button
              onClick={refresh}
              className="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm font-medium"
            >
              Reintentar
            </button>
          </div>
        )}

        {data && !loading && (
          <>
            {data.habits_summary.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 text-center shadow-sm">
                <p className="text-4xl mb-3">🌱</p>
                <p className="text-gray-500 text-sm mb-4">
                  No tienes hábitos activos. ¡Crea el primero!
                </p>
                <button
                  onClick={() => setIsCreateModalOpen(true)}
                  className="text-blue-500 text-sm font-medium"
                >
                  + Crear hábito
                </button>
              </div>
            ) : filteredHabits.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 text-center shadow-sm">
                <p className="text-3xl mb-3">🔍</p>
                <p className="text-gray-500 text-sm mb-3">
                  Ningún hábito coincide con los filtros.
                </p>
                {hasActiveFilters && (
                  <button
                    onClick={() => { setSearch(''); setCategoryFilter(''); setFrequencyFilter('') }}
                    className="text-blue-500 text-sm font-medium"
                  >
                    Limpiar filtros
                  </button>
                )}
              </div>
            ) : (
              <div className="flex flex-col gap-3">
                {filteredHabits.map((habit) => (
                  <HabitCard
                    key={habit.habit_id}
                    habit={habit}
                    onCheckin={handleCheckin}
                    isCheckedInToday={isCheckedInToday(habit)}
                  />
                ))}
              </div>
            )}
          </>
        )}
      </div>

      <button
        onClick={() => setIsCreateModalOpen(true)}
        className="fixed bottom-20 right-4 z-40 w-14 h-14 bg-blue-500 hover:bg-blue-600 text-white rounded-full shadow-lg flex items-center justify-center text-2xl active:scale-95 transition-transform"
        aria-label="Crear hábito"
      >
        +
      </button>

      <BottomNav />

      <CreateHabitModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onHabitCreated={() => {
          refresh()
          setIsCreateModalOpen(false)
        }}
      />

      <StreakCelebration
        streak={celebration.streak}
        isVisible={celebration.visible}
        onComplete={() => setCelebration({ visible: false, streak: 0 })}
      />
    </div>
  )
}
