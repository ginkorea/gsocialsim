import type { RunInfo } from '@/lib/types'

interface Props {
  runs: RunInfo[]
}

function flattenConfig(config: Record<string, unknown>): Record<string, unknown> {
  const flat: Record<string, unknown> = {}
  for (const [key, value] of Object.entries(config)) {
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      for (const [subKey, subValue] of Object.entries(value as Record<string, unknown>)) {
        flat[`${key}.${subKey}`] = subValue
      }
    } else {
      flat[key] = value
    }
  }
  return flat
}

export function ParamDiff({ runs }: Props) {
  if (runs.length < 2) return null

  const configs = runs.map((r) => flattenConfig(r.config as unknown as Record<string, unknown>))
  const allKeys = Array.from(new Set(configs.flatMap(Object.keys))).sort()

  // Only show keys that differ
  const diffKeys = allKeys.filter((key) => {
    const vals = configs.map((c) => JSON.stringify(c[key]))
    return new Set(vals).size > 1
  })

  if (diffKeys.length === 0) {
    return (
      <div className="glass rounded-xl p-4 text-center text-muted-foreground text-sm">
        No parameter differences found
      </div>
    )
  }

  return (
    <div className="glass rounded-xl p-4 overflow-auto">
      <h3 className="text-sm font-medium mb-3">Parameter Differences</h3>
      <table className="w-full text-xs">
        <thead>
          <tr className="border-b border-border">
            <th className="text-left py-2 px-2 text-muted-foreground font-medium">Parameter</th>
            {runs.map((r) => (
              <th key={r.id} className="text-left py-2 px-2 text-muted-foreground font-medium">
                {r.id}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {diffKeys.map((key) => (
            <tr key={key} className="border-b border-border/50 hover:bg-zinc-800/50">
              <td className="py-1.5 px-2 text-muted-foreground">{key}</td>
              {configs.map((c, i) => (
                <td key={runs[i].id} className="py-1.5 px-2 tabular-nums text-yellow-400">
                  {JSON.stringify(c[key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
