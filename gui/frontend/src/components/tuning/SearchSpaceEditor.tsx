import { useCallback } from 'react'
import type { ParamDef } from '@/lib/types'
import { useParams } from '@/hooks/useParams'

interface SearchSpaceEntry {
  enabled: boolean
  low: number
  high: number
  type: string
}

interface Props {
  space: Record<string, SearchSpaceEntry>
  onChange: (space: Record<string, SearchSpaceEntry>) => void
}

export function SearchSpaceEditor({ space, onChange }: Props) {
  const { schema } = useParams()

  const toggleParam = useCallback(
    (name: string, param: ParamDef) => {
      const current = space[name]
      if (current) {
        const updated = { ...space }
        delete updated[name]
        onChange(updated)
      } else {
        onChange({
          ...space,
          [name]: {
            enabled: true,
            low: (param.min ?? 0),
            high: (param.max ?? 1),
            type: param.type === 'int' ? 'int' : 'float',
          },
        })
      }
    },
    [space, onChange]
  )

  const updateRange = useCallback(
    (name: string, field: 'low' | 'high', value: number) => {
      const entry = space[name]
      if (!entry) return
      onChange({
        ...space,
        [name]: { ...entry, [field]: value },
      })
    },
    [space, onChange]
  )

  if (!schema) return null

  const tunableGroups = ['Belief Dynamics', 'Kernel', 'Feed Algorithm', 'Broadcast Feed', 'Media Diet']

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-medium">Search Space</h3>
      {tunableGroups.map((groupName) => {
        const params = schema.groups[groupName]
        if (!params) return null
        return (
          <div key={groupName} className="glass rounded-lg p-3">
            <div className="text-xs text-muted-foreground mb-2">{groupName}</div>
            {params
              .filter((p) => p.type === 'float' || p.type === 'int')
              .map((p) => {
                const entry = space[p.name]
                return (
                  <div key={p.name} className="flex items-center gap-2 py-1">
                    <input
                      type="checkbox"
                      checked={!!entry}
                      onChange={() => toggleParam(p.name, p)}
                      className="rounded border-border accent-primary"
                    />
                    <span className="w-36 text-xs truncate">{p.display_name}</span>
                    {entry && (
                      <>
                        <input
                          type="number"
                          value={entry.low}
                          onChange={(e) => updateRange(p.name, 'low', parseFloat(e.target.value))}
                          className="w-16 px-1 py-0.5 text-xs bg-zinc-800 border border-border rounded"
                          step={p.step}
                        />
                        <span className="text-xs text-muted-foreground">to</span>
                        <input
                          type="number"
                          value={entry.high}
                          onChange={(e) => updateRange(p.name, 'high', parseFloat(e.target.value))}
                          className="w-16 px-1 py-0.5 text-xs bg-zinc-800 border border-border rounded"
                          step={p.step}
                        />
                      </>
                    )}
                  </div>
                )
              })}
          </div>
        )
      })}
    </div>
  )
}
