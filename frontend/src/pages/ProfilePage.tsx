import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { updateProfile, changePassword } from '../api/auth'
import BottomNav from '../components/layout/BottomNav'

export default function ProfilePage() {
  const navigate = useNavigate()
  const { userEmail, username, logout, refreshProfile } = useAuth()

  const [editingUsername, setEditingUsername] = useState(false)
  const [newUsername, setNewUsername] = useState(username ?? '')
  const [usernameLoading, setUsernameLoading] = useState(false)
  const [usernameError, setUsernameError] = useState<string | null>(null)
  const [usernameSuccess, setUsernameSuccess] = useState(false)

  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [passwordLoading, setPasswordLoading] = useState(false)
  const [passwordError, setPasswordError] = useState<string | null>(null)
  const [passwordSuccess, setPasswordSuccess] = useState(false)
  const [showCurrent, setShowCurrent] = useState(false)
  const [showNew, setShowNew] = useState(false)

  const initials = (username ?? userEmail ?? '?')
    .slice(0, 2)
    .toUpperCase()

  const handleUpdateUsername = async (e: React.FormEvent) => {
    e.preventDefault()
    const trimmed = newUsername.trim()
    if (trimmed.length < 3) {
      setUsernameError('Mínimo 3 caracteres')
      return
    }
    if (trimmed === username) {
      setEditingUsername(false)
      return
    }
    setUsernameLoading(true)
    setUsernameError(null)
    try {
      await updateProfile(trimmed)
      await refreshProfile()
      setEditingUsername(false)
      setUsernameSuccess(true)
      setTimeout(() => setUsernameSuccess(false), 3000)
    } catch (err) {
      setUsernameError(err instanceof Error ? err.message : 'Error actualizando perfil')
    } finally {
      setUsernameLoading(false)
    }
  }

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault()
    if (newPassword.length < 8) {
      setPasswordError('La nueva contraseña debe tener al menos 8 caracteres')
      return
    }
    if (newPassword !== confirmPassword) {
      setPasswordError('Las contraseñas no coinciden')
      return
    }
    setPasswordLoading(true)
    setPasswordError(null)
    try {
      await changePassword(currentPassword, newPassword)
      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
      setPasswordSuccess(true)
      setTimeout(() => setPasswordSuccess(false), 3000)
    } catch (err) {
      setPasswordError(err instanceof Error ? err.message : 'Error cambiando contraseña')
    } finally {
      setPasswordLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      {/* Header */}
      <div className="bg-white px-4 pt-12 pb-6 shadow-sm">
        <h1 className="text-xl font-bold text-gray-900 mb-6">Perfil</h1>
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-blue-500 flex items-center justify-center text-white text-xl font-bold shrink-0">
            {initials}
          </div>
          <div>
            <p className="text-base font-semibold text-gray-900">{username ?? '—'}</p>
            <p className="text-sm text-gray-500">{userEmail}</p>
          </div>
        </div>
      </div>

      <div className="px-4 py-4 space-y-4 max-w-lg mx-auto">
        {/* Edit username */}
        <div className="bg-white rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-800">Nombre de usuario</h2>
            {!editingUsername && (
              <button
                onClick={() => { setEditingUsername(true); setNewUsername(username ?? '') }}
                className="text-xs text-blue-600 font-medium"
              >
                Editar
              </button>
            )}
          </div>

          {editingUsername ? (
            <form onSubmit={handleUpdateUsername} className="flex flex-col gap-3">
              <div className="flex items-center border-b border-gray-300 focus-within:border-blue-500">
                <input
                  type="text"
                  value={newUsername}
                  onChange={(e) => setNewUsername(e.target.value.slice(0, 100))}
                  className="flex-1 bg-transparent py-2 text-gray-900 text-sm focus:outline-none"
                  autoFocus
                />
                <span className="text-xs text-gray-400 shrink-0">{newUsername.length}/100</span>
              </div>
              {usernameError && <p className="text-xs text-red-500">{usernameError}</p>}
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => { setEditingUsername(false); setUsernameError(null) }}
                  className="flex-1 py-2 rounded-xl border border-gray-200 text-sm text-gray-600 font-medium"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={usernameLoading}
                  className="flex-1 py-2 rounded-xl bg-blue-500 text-white text-sm font-medium disabled:opacity-60"
                >
                  {usernameLoading ? 'Guardando…' : 'Guardar'}
                </button>
              </div>
            </form>
          ) : (
            <p className="text-sm text-gray-700">{username ?? '—'}</p>
          )}

          {usernameSuccess && (
            <p className="text-xs text-green-600 mt-2">Nombre actualizado</p>
          )}
        </div>

        {/* Change password */}
        <div className="bg-white rounded-2xl p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-800 mb-4">Cambiar contraseña</h2>
          <form onSubmit={handleChangePassword} className="flex flex-col gap-4">
            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wide font-medium">
                Contraseña actual
              </label>
              <div className="flex items-center border-b border-gray-300 focus-within:border-blue-500">
                <input
                  type={showCurrent ? 'text' : 'password'}
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="flex-1 bg-transparent py-2 text-gray-900 text-sm focus:outline-none"
                />
                <button
                  type="button"
                  onClick={() => setShowCurrent(v => !v)}
                  className="text-gray-400 text-xs shrink-0 px-1"
                >
                  {showCurrent ? 'Ocultar' : 'Ver'}
                </button>
              </div>
            </div>

            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wide font-medium">
                Nueva contraseña
              </label>
              <div className="flex items-center border-b border-gray-300 focus-within:border-blue-500">
                <input
                  type={showNew ? 'text' : 'password'}
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="flex-1 bg-transparent py-2 text-gray-900 text-sm focus:outline-none"
                />
                <button
                  type="button"
                  onClick={() => setShowNew(v => !v)}
                  className="text-gray-400 text-xs shrink-0 px-1"
                >
                  {showNew ? 'Ocultar' : 'Ver'}
                </button>
              </div>
            </div>

            <div>
              <label className="text-xs text-gray-500 uppercase tracking-wide font-medium">
                Confirmar nueva contraseña
              </label>
              <div className="border-b border-gray-300 focus-within:border-blue-500">
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full bg-transparent py-2 text-gray-900 text-sm focus:outline-none"
                />
              </div>
            </div>

            {passwordError && <p className="text-xs text-red-500">{passwordError}</p>}
            {passwordSuccess && <p className="text-xs text-green-600">Contraseña actualizada</p>}

            <button
              type="submit"
              disabled={passwordLoading || !currentPassword || !newPassword || !confirmPassword}
              className="w-full py-2.5 rounded-xl bg-blue-500 text-white text-sm font-medium disabled:opacity-50 mt-1"
            >
              {passwordLoading ? 'Actualizando…' : 'Actualizar contraseña'}
            </button>
          </form>
        </div>

        {/* Logout */}
        <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
          <button
            onClick={handleLogout}
            className="w-full text-left px-5 py-4 text-sm text-red-500 font-medium"
          >
            Cerrar sesión
          </button>
        </div>
      </div>

      <BottomNav />
    </div>
  )
}
