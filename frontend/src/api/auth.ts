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

export async function getMe(): Promise<User> {
  try {
    const { data } = await client.get<User>('/auth/me')
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Error cargando perfil')
    }
    throw error
  }
}

export async function updateProfile(username: string): Promise<User> {
  try {
    const { data } = await client.patch<User>('/auth/me', { username })
    return data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Error actualizando perfil')
    }
    throw error
  }
}

export async function changePassword(currentPassword: string, newPassword: string): Promise<void> {
  try {
    await client.patch('/auth/me/password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail ?? 'Error cambiando contraseña')
    }
    throw error
  }
}
