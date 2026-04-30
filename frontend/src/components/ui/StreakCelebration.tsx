import { useEffect } from 'react'

interface StreakCelebrationProps {
  streak: number
  isVisible: boolean
  onComplete: () => void
}

export default function StreakCelebration({
  streak,
  isVisible,
  onComplete,
}: StreakCelebrationProps) {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(onComplete, 2000)
      return () => clearTimeout(timer)
    }
  }, [isVisible, onComplete])

  if (!isVisible) return null

  return (
    <div className="fixed inset-0 z-60 flex items-center justify-center pointer-events-none">
      <div
        className="flex flex-col items-center gap-2 animate-streak-pop"
        style={{
          animation: 'streakPop 2s ease-out forwards',
        }}
      >
        <span className="text-7xl">🔥</span>
        <p className="text-4xl font-bold text-orange-500 drop-shadow-lg">
          {streak}
        </p>
        <p className="text-lg font-semibold text-gray-800 bg-white/90 px-4 py-1 rounded-full shadow">
          {streak} días seguidos!
        </p>
      </div>

      <style>{`
        @keyframes streakPop {
          0% {
            opacity: 0;
            transform: translateY(40px) scale(0.7);
          }
          20% {
            opacity: 1;
            transform: translateY(0px) scale(1.1);
          }
          35% {
            transform: scale(1);
          }
          70% {
            opacity: 1;
            transform: scale(1);
          }
          100% {
            opacity: 0;
            transform: translateY(-20px) scale(0.9);
          }
        }
      `}</style>
    </div>
  )
}
