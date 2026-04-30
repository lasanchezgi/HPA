import axios from 'axios'
import client from './client'
import type { Habit, DashboardSummary } from '../types'

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
