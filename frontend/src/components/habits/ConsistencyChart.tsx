import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { consistencyLabel } from '../../utils/consistency'
import type { ConsistencyDataPoint } from '../../types'

interface ConsistencyChartProps {
  data: ConsistencyDataPoint[]
  overallRate: number
}

export default function ConsistencyChart({ data, overallRate }: ConsistencyChartProps) {
  const label = consistencyLabel(overallRate)

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">
          Consistencia
        </span>
        <div className="flex items-center gap-2">
          <span className="text-2xl font-bold text-blue-600">{overallRate}%</span>
          <span className="text-xs text-gray-400 font-medium">{label}</span>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={180}>
        <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="consistencyGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="week" tick={{ fontSize: 11 }} />
          <YAxis
            domain={[0, 100]}
            tickFormatter={(v) => `${v}%`}
            tick={{ fontSize: 11 }}
          />
          <Tooltip formatter={(value) => [`${value}%`, 'Consistencia']} />
          <Area
            type="monotone"
            dataKey="rate"
            stroke="#3B82F6"
            strokeWidth={2}
            fill="url(#consistencyGradient)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
