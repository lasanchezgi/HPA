import { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { useHabits } from '../hooks/useHabits'
import { logCompletion } from '../api/habits'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import StreakCelebration from '../components/ui/StreakCelebration'
import BottomNav from '../components/layout/BottomNav'
import CreateHabitModal from '../components/habits/CreateHabitModal'
import HabitCard from '../components/habits/HabitCard'
import type { HabitSummary, LogCompletionResponse } from '../types'

export default function DashboardPage() {
  const { userEmail, logout } = useAuth()
  const { data, loading, error, refresh } = useHabits()
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [celebration, setCelebration] = useState<{ visible: boolean; streak: number }>({
    visible: false,
    streak: 0,
  })

  const displayName = userEmail?.split('@')[0] ?? 'there'

  const isCheckedInToday = (habit: HabitSummary): boolean => {
    if (!habit.last_logged) return false
    const lastDate = new Date(habit.last_logged).toDateString()
    const today = new Date().toDateString()
    return lastDate === today
  }

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
      <div className="bg-white px-6 pt-12 pb-6 shadow-sm">
        <div className="flex items-center justify-between max-w-sm mx-auto">
          <div>
            <p className="text-gray-400 text-sm">Good day,</p>
            <h2 className="text-xl font-bold text-gray-900">{displayName}!</h2>
          </div>
          <button
            onClick={logout}
            className="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 hover:bg-gray-200"
            title="Logout"
          >
            ⚙️
          </button>
        </div>
      </div>

      <div className="max-w-sm mx-auto px-6 mt-6">
        {loading && (
          <div className="flex justify-center py-16">
            <LoadingSpinner size="lg" />
          </div>
        )}

        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm text-center">
            {error}
          </div>
        )}

        {data && (
          <>
            <div className="grid grid-cols-3 gap-3 mb-6">
              <MetricCard
                label="Streak"
                value={String(data.best_streak_overall)}
                unit="days"
                color="bg-orange-50 text-orange-500"
              />
              <MetricCard
                label="Gems"
                value={String(data.total_gems)}
                unit="total"
                color="bg-purple-50 text-purple-500"
              />
              <MetricCard
                label="Habits"
                value={String(data.total_habits)}
                unit="active"
                color="bg-blue-50 text-blue-500"
              />
            </div>

            {data.consistency_score && (
              <div className="bg-white rounded-2xl p-4 mb-6 shadow-sm">
                <p className="text-xs text-gray-400 font-medium uppercase tracking-wide mb-1">
                  Consistency
                </p>
                <div className="flex items-end gap-2">
                  <span className="text-3xl font-bold text-gray-900">
                    {data.consistency_score.value}%
                  </span>
                  <span className="text-sm text-gray-400 mb-1">
                    {data.consistency_score.label}
                  </span>
                </div>
              </div>
            )}

            <h3 className="text-sm font-semibold text-gray-700 mb-3">Your Habits</h3>

            {data.habits_summary.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 text-center shadow-sm">
                <p className="text-4xl mb-3">🌱</p>
                <p className="text-gray-500 text-sm mb-4">No habits yet</p>
                <button
                  onClick={() => setIsCreateModalOpen(true)}
                  className="text-blue-500 text-sm font-medium"
                >
                  + Create your first habit
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
        aria-label="Create habit"
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

function MetricCard({
  label,
  value,
  unit,
  color,
}: {
  label: string
  value: string
  unit: string
  color: string
}) {
  return (
    <div className={`rounded-2xl p-3 ${color.split(' ')[0]}`}>
      <p className={`text-xs font-medium ${color.split(' ')[1]} opacity-70`}>{label}</p>
      <p className={`text-2xl font-bold ${color.split(' ')[1]}`}>{value}</p>
      <p className={`text-xs ${color.split(' ')[1]} opacity-60`}>{unit}</p>
    </div>
  )
}
