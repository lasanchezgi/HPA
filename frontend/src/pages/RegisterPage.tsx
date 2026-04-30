import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'

export default function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [repeatPassword, setRepeatPassword] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)

  const validate = () => {
    const newErrors: Record<string, string> = {}
    if (!email) newErrors.email = 'El email es requerido'
    if (!username || username.length < 3) newErrors.username = 'Mínimo 3 caracteres'
    if (!password) newErrors.password = 'La contraseña es requerida'
    if (password.length < 8) newErrors.password = 'Mínimo 8 caracteres'
    if (password !== repeatPassword) newErrors.repeatPassword = 'Las contraseñas no coinciden'
    return newErrors
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const validationErrors = validate()
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors)
      return
    }
    setErrors({})
    setLoading(true)
    try {
      await register(email, password, username)
      navigate('/login', { state: { message: '¡Cuenta creada! Inicia sesión para continuar.' } })
    } catch (err) {
      setErrors({ submit: err instanceof Error ? err.message : 'Error al registrarse' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white flex flex-col px-8 pt-16 pb-8 max-w-sm mx-auto">
      <div className="flex justify-between items-start mb-12">
        <div>
          <h1 className="text-5xl font-bold text-gray-900 leading-none">Almost</h1>
          <p className="text-2xl text-gray-400 mt-1">ready...</p>
        </div>
        <div className="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold text-sm">
          HP
        </div>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-5 flex-1">
        <Input
          label="Email"
          type="email"
          value={email}
          onChange={setEmail}
          error={errors.email}
          placeholder="you@example.com"
        />
        <Input
          label="Name"
          value={name}
          onChange={setName}
          placeholder="Your name"
        />
        <Input
          label="Username"
          value={username}
          onChange={setUsername}
          error={errors.username}
          placeholder="mínimo 3 caracteres"
        />
        <Input
          label="Password"
          type="password"
          value={password}
          onChange={setPassword}
          error={errors.password}
          placeholder="••••••••"
        />
        <Input
          label="Repeat Password"
          type="password"
          value={repeatPassword}
          onChange={setRepeatPassword}
          error={errors.repeatPassword}
          placeholder="••••••••"
        />

        {errors.submit && (
          <p className="text-sm text-red-500 text-center">{errors.submit}</p>
        )}

        <Button type="submit" isLoading={loading} className="mt-2">
          Sign up
        </Button>

        <p className="text-center text-sm text-gray-400 mt-auto">
          I already have an account{' '}
          <Link to="/login" className="text-blue-500 font-medium">
            Login
          </Link>
        </p>
      </form>
    </div>
  )
}
