export interface User {
  id: string
  email: string
  created_at: string
}

export interface AuthTokens {
  access_token: string
  token_type: string
}

export interface Habit {
  id: string
  habit_name: string
  habit_description: string | null
  frequency_code: string
  category_code: string
  is_active: boolean
  habit_start_date: string
  created_at: string
}

export interface Streak {
  current_streak: number
  best_streak: number
}

export interface HabitSummary {
  habit_id: string
  habit_name: string
  current_streak: number
  last_logged: string | null
}

export interface ConsistencyScore {
  value: number
  label: string
}

export interface DashboardSummary {
  total_habits: number
  active_streaks: number
  best_streak_overall: number
  consistency_score: ConsistencyScore
  total_gems: number
  habits_summary: HabitSummary[]
}

export interface CreateHabitPayload {
  habit_name: string
  habit_description?: string
  frequency_code: string
  category_code: string
}

export interface LogCompletionPayload {
  status: 'done' | 'partial' | 'not_done'
  notes?: string
}

export interface LogCompletionResponse {
  log_id: string
  habit_id: string
  status: string
  current_streak: number
  best_streak: number
  logged_at: string
}

export interface CreatedHabit {
  id: string
  habit_name: string
  habit_description: string | null
  frequency_code: string
  category_code: string
  is_active: boolean
  habit_start_date: string
  created_at: string
}
