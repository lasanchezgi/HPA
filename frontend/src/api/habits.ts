import axios from 'axios'
import client from './client'
import type {
  Habit,
  DashboardSummary,
  CreateHabitPayload,
  CreatedHabit,
  LogCompletionPayload,
  LogCompletionResponse,
  HabitDetail,
  HabitLog,
  UpdateHabitPayload,
} from '../types'

export async function getHabits(): Promise<Habit[]> {
  try {
    const { data } = await client.get<Habit[]>('/habits/')
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Error cargando hábitos')
    }
    throw error
  }
}

export async function getDashboard(): Promise<DashboardSummary> {
  try {
    const { data } = await client.get<DashboardSummary>('/dashboard/')
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Error cargando el dashboard')
    }
    throw error
  }
}

export const createHabit = async (
  payload: CreateHabitPayload
): Promise<CreatedHabit> => {
  try {
    const { data } = await client.post('/habits/', payload)
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        error.response?.data?.detail ?? 'Error creando el hábito'
      )
    }
    throw error
  }
}

export const getHabitDetail = async (habitId: string): Promise<HabitDetail> => {
  try {
    const { data } = await client.get(`/habits/${habitId}`)
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Hábito no encontrado')
    }
    throw error
  }
}

export const getHabitLogs = async (habitId: string): Promise<HabitLog[]> => {
  try {
    const { data } = await client.get(`/habits/${habitId}/logs`)
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Error cargando historial')
    }
    throw error
  }
}

export const updateHabit = async (
  habitId: string,
  payload: UpdateHabitPayload
): Promise<HabitDetail> => {
  try {
    const { data } = await client.put(`/habits/${habitId}`, payload)
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Error actualizando el hábito')
    }
    throw error
  }
}

export const archiveHabit = async (habitId: string): Promise<void> => {
  try {
    await client.patch(`/habits/${habitId}/archive`)
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Error archivando el hábito')
    }
    throw error
  }
}

export const logCompletion = async (
  habitId: string,
  payload: LogCompletionPayload
): Promise<LogCompletionResponse> => {
  try {
    const { data } = await client.post(`/habits/${habitId}/logs`, payload)
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status
      if (status === 409) {
        throw new Error('Ya registraste este hábito hoy')
      }
      throw new Error(
        error.response?.data?.detail ?? 'Error registrando el hábito'
      )
    }
    throw error
  }
}
