import { createContext, useState, useEffect, type ReactNode } from 'react'
import { login as apiLogin, register as apiRegister, getMe } from '../api/auth'

interface AuthContextType {
  isAuthenticated: boolean
  userEmail: string | null
  username: string | null
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, username: string) => Promise<void>
  logout: () => void
  refreshProfile: () => Promise<void>
}

export const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [userEmail, setUserEmail] = useState<string | null>(null)
  const [username, setUsername] = useState<string | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    const email = localStorage.getItem('user_email')
    const storedUsername = localStorage.getItem('username')
    if (token) {
      setIsAuthenticated(true)
      setUserEmail(email)
      setUsername(storedUsername)
    }
  }, [])

  const login = async (email: string, password: string) => {
    await apiLogin(email, password)
    localStorage.setItem('user_email', email)
    setIsAuthenticated(true)
    setUserEmail(email)
    // fetch profile to get username
    try {
      const user = await getMe()
      localStorage.setItem('username', user.username)
      setUsername(user.username)
    } catch {
      // non-blocking
    }
  }

  const register = async (email: string, password: string, username: string) => {
    await apiRegister(email, password, username)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_email')
    localStorage.removeItem('username')
    setIsAuthenticated(false)
    setUserEmail(null)
    setUsername(null)
  }

  const refreshProfile = async () => {
    try {
      const user = await getMe()
      localStorage.setItem('username', user.username)
      localStorage.setItem('user_email', user.email)
      setUsername(user.username)
      setUserEmail(user.email)
    } catch {
      // non-blocking
    }
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, userEmail, username, login, register, logout, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  )
}
