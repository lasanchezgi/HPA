interface InputProps {
  label: string
  type?: string
  value: string
  onChange: (value: string) => void
  error?: string
  placeholder?: string
}

export default function Input({
  label,
  type = 'text',
  value,
  onChange,
  error,
  placeholder,
}: InputProps) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
        {label}
      </label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className={`
          border-0 border-b bg-transparent py-2 px-0 text-gray-900
          focus:outline-none focus:ring-0 focus:border-blue-500
          placeholder:text-gray-300 text-sm
          ${error ? 'border-red-400' : 'border-gray-300'}
        `}
      />
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  )
}
