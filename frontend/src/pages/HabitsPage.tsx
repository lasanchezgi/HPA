import { useState } from 'react'
import { useHabits } from '../hooks/useHabits'
import { logCompletion } from '../api/habits'
import HabitCard from '../components/habits/HabitCard'
import CreateHabitModal from '../components/habits/CreateHabitModal'
import BottomNav from '../components/layout/BottomNav'
import StreakCelebration from '../components/ui/StreakCelebration'
import type { HabitSummary, LogCompletionResponse } from '../types'

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

const isCheckedInToday = (habit: HabitSummary): boolean => {
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
        <h1 className="text-xl font-bold text-gray-900">Mis hábitos</h1>
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
            ) : (
              <div className="flex flex-col gap-3">
                {data.habits_summary.map((habit) => (
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
