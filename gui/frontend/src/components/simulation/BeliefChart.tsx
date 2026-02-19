import { useMemo } from 'react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
} from 'recharts'
import { useRunStore } from '@/stores/runStore'

const BINS = 20
const BIN_EDGES = Array.from({ length: BINS + 1 }, (_, i) => -1 + (2 * i) / BINS)

function buildHistogram(leans: number[]): Record<string, number> {
  const counts: Record<string, number> = {}
  for (let i = 0; i < BINS; i++) {
    counts[`bin${i}`] = 0
  }
  for (const lean of leans) {
    const idx = Math.min(Math.floor(((lean + 1) / 2) * BINS), BINS - 1)
    counts[`bin${Math.max(0, idx)}`]++
  }
  return counts
}

export function BeliefChart() {
  const tickHistory = useRunStore((s) => s.tickHistory)

  const data = useMemo(() => {
    // Sample every N ticks to avoid too many data points
    const step = Math.max(1, Math.floor(tickHistory.length / 100))
    return tickHistory
      .filter((_, i) => i % step === 0 || i === tickHistory.length - 1)
      .map((t) => ({
        tick: t.tick,
        ...buildHistogram(t.leans),
      }))
  }, [tickHistory])

  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-muted-foreground text-sm">
        Waiting for simulation data...
      </div>
    )
  }

  const colors = Array.from({ length: BINS }, (_, i) => {
    const center = BIN_EDGES[i] + 1 / BINS
    if (center < 0) {
      const t = Math.abs(center)
      return `rgba(59,130,246,${0.2 + t * 0.8})`
    } else {
      const t = center
      return `rgba(239,68,68,${0.2 + t * 0.8})`
    }
  })

  return (
    <div className="glass rounded-xl p-4">
      <h3 className="text-sm font-medium mb-3">Political Lean Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <XAxis
            dataKey="tick"
            stroke="#71717a"
            tick={{ fontSize: 10, fill: '#a1a1aa' }}
          />
          <YAxis stroke="#71717a" tick={{ fontSize: 10, fill: '#a1a1aa' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#18181b',
              border: '1px solid #3f3f46',
              borderRadius: '8px',
              fontSize: 12,
            }}
          />
          {Array.from({ length: BINS }, (_, i) => (
            <Area
              key={i}
              type="monotone"
              dataKey={`bin${i}`}
              stackId="1"
              fill={colors[i]}
              stroke="none"
            />
          ))}
        </AreaChart>
      </ResponsiveContainer>
      <div className="flex justify-between text-xs text-muted-foreground mt-1 px-2">
        <span>Left (-1)</span>
        <span>Center (0)</span>
        <span>Right (+1)</span>
      </div>
    </div>
  )
}
