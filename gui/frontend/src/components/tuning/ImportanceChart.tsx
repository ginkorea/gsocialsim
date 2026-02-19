import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
} from 'recharts'

interface Props {
  importance: Record<string, number>
}

export function ImportanceChart({ importance }: Props) {
  const data = Object.entries(importance)
    .sort(([, a], [, b]) => b - a)
    .map(([name, value]) => ({ name, value: Math.round(value * 100) }))

  if (data.length === 0) {
    return (
      <div className="glass rounded-xl p-4">
        <h3 className="text-sm font-medium mb-3">Parameter Importance</h3>
        <div className="flex items-center justify-center h-40 text-muted-foreground text-sm">
          Need more trials to compute importance
        </div>
      </div>
    )
  }

  return (
    <div className="glass rounded-xl p-4">
      <h3 className="text-sm font-medium mb-3">Parameter Importance</h3>
      <ResponsiveContainer width="100%" height={Math.max(150, data.length * 30)}>
        <BarChart data={data} layout="vertical">
          <XAxis type="number" stroke="#71717a" tick={{ fontSize: 10, fill: '#a1a1aa' }} domain={[0, 100]} />
          <YAxis type="category" dataKey="name" stroke="#71717a" tick={{ fontSize: 10, fill: '#a1a1aa' }} width={140} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#18181b',
              border: '1px solid #3f3f46',
              borderRadius: '8px',
              fontSize: 12,
            }}
          />
          <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
