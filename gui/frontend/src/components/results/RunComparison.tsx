import type { RunInfo } from '@/lib/types'

interface Props {
  runs: RunInfo[]
}

export function RunComparison({ runs }: Props) {
  if (runs.length === 0) {
    return (
      <div className="glass rounded-xl p-6 text-center text-muted-foreground text-sm">
        Select runs to compare
      </div>
    )
  }

  const metricKeys = Array.from(
    new Set(runs.flatMap((r) => Object.keys(r.metrics || {})))
  ).filter((k) => k !== 'error')

  return (
    <div className="glass rounded-xl p-4 overflow-auto">
      <h3 className="text-sm font-medium mb-3">Run Comparison</h3>
      <table className="w-full text-xs">
        <thead>
          <tr className="border-b border-border">
            <th className="text-left py-2 px-2 text-muted-foreground font-medium">Metric</th>
            {runs.map((r) => (
              <th key={r.id} className="text-left py-2 px-2 text-muted-foreground font-medium">
                {r.id}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr className="border-b border-border/50">
            <td className="py-1.5 px-2 text-muted-foreground">Status</td>
            {runs.map((r) => (
              <td key={r.id} className="py-1.5 px-2">
                {r.status}
              </td>
            ))}
          </tr>
          <tr className="border-b border-border/50">
            <td className="py-1.5 px-2 text-muted-foreground">Ticks</td>
            {runs.map((r) => (
              <td key={r.id} className="py-1.5 px-2 tabular-nums">
                {r.ticks_completed}/{r.total_ticks}
              </td>
            ))}
          </tr>
          {metricKeys.map((key) => (
            <tr key={key} className="border-b border-border/50 hover:bg-zinc-800/50">
              <td className="py-1.5 px-2 text-muted-foreground">{key}</td>
              {runs.map((r) => (
                <td key={r.id} className="py-1.5 px-2 tabular-nums">
                  {r.metrics?.[key] !== undefined
                    ? typeof r.metrics[key] === 'number'
                      ? Number(r.metrics[key]).toFixed(4)
                      : String(r.metrics[key])
                    : '-'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
