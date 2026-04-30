import type { ReactNode } from 'react'
import LoadingSpinner from './LoadingSpinner'

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost'
  isLoading?: boolean
  children: ReactNode
  onClick?: () => void
  type?: 'button' | 'submit'
  disabled?: boolean
  className?: string
}

const variantClasses = {
  primary: 'bg-blue-500 hover:bg-blue-600 text-white border-transparent',
  secondary: 'bg-transparent hover:bg-gray-50 text-blue-500 border-blue-500',
  ghost: 'bg-transparent hover:bg-gray-100 text-gray-600 border-transparent',
}

export default function Button({
  variant = 'primary',
  isLoading = false,
  children,
  onClick,
  type = 'button',
  disabled = false,
  className = '',
}: ButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || isLoading}
      className={`
        w-full flex items-center justify-center gap-2
        rounded-full px-6 py-3 text-sm font-semibold
        border transition-colors duration-150
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variantClasses[variant]}
        ${className}
      `}
    >
      {isLoading && <LoadingSpinner size="sm" />}
      {children}
    </button>
  )
}
