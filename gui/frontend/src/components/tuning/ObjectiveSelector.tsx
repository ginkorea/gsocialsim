const OBJECTIVES = [
  { name: 'polarization', label: 'Polarization (variance of leans)', defaultDir: 'minimize' },
  { name: 'crossing_rate', label: 'Crossing Rate (deltas/tick)', defaultDir: 'maximize' },
  { name: 'consumption_rate', label: 'Consumption Rate', defaultDir: 'maximize' },
  { name: 'mean_belief_shift', label: 'Mean Belief Shift', defaultDir: 'maximize' },
  { name: 'influence_gini', label: 'Influence Gini', defaultDir: 'minimize' },
]

interface ObjectiveConfig {
  name: string
  direction: string
}

interface Props {
  objectives: ObjectiveConfig[]
  onChange: (objectives: ObjectiveConfig[]) => void
}

export function ObjectiveSelector({ objectives, onChange }: Props) {
  const toggle = (name: string, defaultDir: string) => {
    const idx = objectives.findIndex((o) => o.name === name)
    if (idx >= 0) {
      onChange(objectives.filter((_, i) => i !== idx))
    } else {
      onChange([...objectives, { name, direction: defaultDir }])
    }
  }

  const setDirection = (name: string, direction: string) => {
    onChange(objectives.map((o) => (o.name === name ? { ...o, direction } : o)))
  }

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-medium">Objectives</h3>
      <div className="glass rounded-lg p-3 space-y-2">
        {OBJECTIVES.map((obj) => {
          const selected = objectives.find((o) => o.name === obj.name)
          return (
            <div key={obj.name} className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={!!selected}
                onChange={() => toggle(obj.name, obj.defaultDir)}
                className="rounded border-border accent-primary"
              />
              <span className="flex-1 text-xs">{obj.label}</span>
              {selected && (
                <select
                  value={selected.direction}
                  onChange={(e) => setDirection(obj.name, e.target.value)}
                  className="text-xs bg-zinc-800 border border-border rounded px-1 py-0.5"
                >
                  <option value="minimize">Minimize</option>
                  <option value="maximize">Maximize</option>
                </select>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
