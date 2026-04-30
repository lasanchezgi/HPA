import { createContext, useState, useEffect, type ReactNode } from 'react'
import { login as apiLogin, register as apiRegister } from '../api/auth'

interface AuthContextType {
  isAuthenticated: boolean
  userEmail: string | null
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, username: string) => Promise<void>
  logout: () => void
}

export const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [userEmail, setUserEmail] = useState<string | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    const email = localStorage.getItem('user_email')
    if (token) {
      setIsAuthenticated(true)
      setUserEmail(email)
    }
  }, [])

  const login = async (email: string, password: string) => {
    await apiLogin(email, password)
    localStorage.setItem('user_email', email)
    setIsAuthenticated(true)
    setUserEmail(email)
  }

  const register = async (email: string, password: string, username: string) => {
    await apiRegister(email, password, username)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_email')
    setIsAuthenticated(false)
    setUserEmail(null)
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, userEmail, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
