import { useMemo } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
} from 'recharts'
import { useTuningStore } from '@/stores/tuningStore'

export function OptProgress() {
  const { trials, bestValue, status } = useTuningStore()

  const data = useMemo(() => {
    let runningBest: number | null = null
    return trials.map((t, i) => {
      const val = t.values[0]
      if (runningBest === null || val < runningBest) {
        runningBest = val
      }
      return {
        trial: i + 1,
        value: val,
        best: runningBest,
      }
    })
  }, [trials])

  return (
    <div className="glass rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium">Optimization Progress</h3>
        <div className="flex items-center gap-3 text-xs text-muted-foreground">
          <span>{trials.length} trials</span>
          {bestValue !== null && <span>Best: {bestValue.toFixed(4)}</span>}
          <div className={`w-2 h-2 rounded-full ${status === 'running' ? 'bg-green-500 animate-pulse' : 'bg-zinc-600'}`} />
        </div>
      </div>
      {data.length > 0 ? (
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={data}>
            <XAxis dataKey="trial" stroke="#71717a" tick={{ fontSize: 10, fill: '#a1a1aa' }} />
            <YAxis stroke="#71717a" tick={{ fontSize: 10, fill: '#a1a1aa' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#18181b',
                border: '1px solid #3f3f46',
                borderRadius: '8px',
                fontSize: 12,
              }}
            />
            <Line type="monotone" dataKey="value" stroke="#71717a" dot={{ r: 2 }} strokeWidth={1} />
            <Line type="stepAfter" dataKey="best" stroke="#3b82f6" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <div className="flex items-center justify-center h-[250px] text-muted-foreground text-sm">
          {status === 'running' ? 'Waiting for first trial...' : 'No trials yet'}
        </div>
      )}
    </div>
  )
}
