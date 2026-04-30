import axios from 'axios'
import client from './client'
import type { User, AuthTokens } from '../types'

export async function register(email: string, password: string, username: string): Promise<User> {
  try {
    const { data } = await client.post<User>('/auth/register', { email, password, username })
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Error al registrar usuario')
    }
    throw error
  }
}

export async function login(email: string, password: string): Promise<AuthTokens> {
  try {
    const { data } = await client.post<AuthTokens>('/auth/login', { email, password })
    localStorage.setItem('access_token', data.access_token)
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Credenciales incorrectas')
    }
    throw error
  }
}
