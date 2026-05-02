import axios from 'axios'
import client from './client'
import type { CoachChatResponse, CoachHistoryResponse } from '../types'

export const sendCoachMessage = async (
  message: string
): Promise<CoachChatResponse> => {
  try {
    const { data } = await client.post<CoachChatResponse>('/coach/chat', { message })
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status
      if (status === 429) throw new Error('Coach ocupado. Intenta en unos segundos.')
      if (status === 503) throw new Error('Coach no disponible temporalmente.')
      throw new Error(error.response?.data?.detail ?? 'Error al enviar mensaje.')
    }
    throw error
  }
}

export const getCoachHistory = async (): Promise<CoachHistoryResponse> => {
  try {
    const { data } = await client.get<CoachHistoryResponse>('/coach/history')
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Error cargando historial.')
    }
    throw error
  }
}
