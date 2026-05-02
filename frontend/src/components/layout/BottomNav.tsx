import { NavLink } from 'react-router-dom'

const tabs = [
  { to: '/dashboard', label: 'Home', icon: '🏠' },
  { to: '/habits', label: 'Habits', icon: '✅' },
  { to: '/coach', label: 'Coach', icon: '🤖' },
  { to: '/profile', label: 'Profile', icon: '👤' },
]

export default function BottomNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 flex justify-around py-2 z-10">
      {tabs.map((tab) => (
        <NavLink
          key={tab.to}
          to={tab.to}
          className={({ isActive }) =>
            `flex flex-col items-center gap-0.5 px-4 py-1 text-xs ${
              isActive ? 'text-blue-500' : 'text-gray-400'
            }`
          }
        >
          <span className="text-xl">{tab.icon}</span>
          <span>{tab.label}</span>
        </NavLink>
      ))}
    </nav>
  )
}
