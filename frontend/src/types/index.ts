export interface User {
  id: string
  username: string
  email: string
  is_active: boolean
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

export interface HabitLog {
  id: string
  habit_id: string
  status: 'done' | 'partial' | 'not_done'
  notes: string | null
  logged_at: string  // ISO datetime
}

export interface HabitDetail {
  id: string
  user_id: string
  habit_name: string
  habit_description: string | null
  frequency_id: string
  category_id: string
  frequency_code: string
  category_code: string
  is_active: boolean
  habit_start_date: string
  created_at: string
  current_streak: number
  best_streak: number
}

export interface UpdateHabitPayload {
  habit_name?: string
  habit_description?: string
  frequency_code?: string
  category_code?: string
  goal_target?: number
}

export interface ConsistencyDataPoint {
  week: string
  completed: number
  total: number
  rate: number
}

export interface CoachMessage {
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface CoachChatResponse {
  reply: string
  conversation_id: string
}

export interface CoachHistoryResponse {
  conversation_id: string
  messages: CoachMessage[]
}
