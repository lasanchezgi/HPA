import { useState, useEffect } from 'react'
import { updateHabit } from '../../api/habits'
import Button from '../ui/Button'
import type { HabitDetail } from '../../types'

interface EditHabitModalProps {
  isOpen: boolean
  habit: HabitDetail
  onClose: () => void
  onHabitUpdated: () => void
}

const FREQUENCIES = [
  { label: 'Diario', code: 'daily' },
  { label: 'Semanal', code: 'weekly' },
  { label: 'Mensual', code: 'monthly' },
]

const CATEGORIES = [
  { label: '💪 Salud', code: 'health' },
  { label: '⚡ Productividad', code: 'productivity' },
  { label: '📚 Aprendizaje', code: 'learning' },
]

export default function EditHabitModal({
  isOpen,
  habit,
  onClose,
  onHabitUpdated,
}: EditHabitModalProps) {
  const [name, setName] = useState(habit.habit_name)
  const [description, setDescription] = useState(habit.habit_description ?? '')
  const [frequency, setFrequency] = useState(habit.frequency_code)
  const [category, setCategory] = useState(habit.category_code)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (isOpen) {
      setName(habit.habit_name)
      setDescription(habit.habit_description ?? '')
      setFrequency(habit.frequency_code)
      setCategory(habit.category_code)
      setError(null)
    }
  }, [isOpen, habit])

  if (!isOpen) return null

  const isValid = name.trim().length > 0 && category !== '' && frequency !== ''
  const hasChanges =
    name.trim() !== habit.habit_name ||
    description.trim() !== (habit.habit_description ?? '') ||
    frequency !== habit.frequency_code ||
    category !== habit.category_code

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!isValid || !hasChanges) return

    setLoading(true)
    setError(null)

    try {
      await updateHabit(habit.id, {
        habit_name: name.trim(),
        habit_description: description.trim() || undefined,
        frequency_code: frequency,
        category_code: category,
      })
      onHabitUpdated()
      onClose()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error actualizando el hábito')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center bg-black/50"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose()
      }}
    >
      <div className="w-full max-w-sm bg-white rounded-t-3xl px-6 pt-6 pb-10 shadow-xl">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-bold text-gray-900">Editar hábito</h2>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 hover:bg-gray-200"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-5">
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
              Nombre
            </label>
            <div className="flex items-center border-b border-gray-300 focus-within:border-blue-500">
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value.slice(0, 100))}
                placeholder="e.g. Meditar"
                className="flex-1 bg-transparent py-2 text-gray-900 text-sm focus:outline-none placeholder:text-gray-300"
              />
              <span className="text-xs text-gray-400 shrink-0">{name.length}/100</span>
            </div>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
              Descripción
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value.slice(0, 200))}
              placeholder="¿Cuál es el objetivo?"
              rows={2}
              className="bg-transparent border-b border-gray-300 focus:border-blue-500 focus:outline-none py-2 text-gray-900 text-sm placeholder:text-gray-300 resize-none"
            />
            <span className="text-xs text-gray-400 text-right">{description.length}/200</span>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
              Frecuencia
            </label>
            <div className="flex gap-2">
              {FREQUENCIES.map((f) => (
                <button
                  key={f.code}
                  type="button"
                  onClick={() => setFrequency(f.code)}
                  className={`flex-1 py-2 rounded-full text-xs font-semibold border transition-colors ${
                    frequency === f.code
                      ? 'bg-blue-500 text-white border-blue-500'
                      : 'bg-white text-gray-600 border-gray-300 hover:border-blue-300'
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
              Categoría
            </label>
            <div className="flex gap-2">
              {CATEGORIES.map((c) => (
                <button
                  key={c.code}
                  type="button"
                  onClick={() => setCategory(c.code)}
                  className={`flex-1 py-2 rounded-full text-xs font-semibold border transition-colors ${
                    category === c.code
                      ? 'bg-blue-500 text-white border-blue-500'
                      : 'bg-white text-gray-600 border-gray-300 hover:border-blue-300'
                  }`}
                >
                  {c.label}
                </button>
              ))}
            </div>
          </div>

          {error && (
            <p className="text-xs text-red-500 text-center">{error}</p>
          )}

          <Button
            type="submit"
            isLoading={loading}
            disabled={!isValid || !hasChanges}
          >
            Guardar cambios
          </Button>
        </form>
      </div>
    </div>
  )
}
