import { useTuningStore } from '@/stores/tuningStore'

interface Props {
  onApply?: (params: Record<string, number>) => void
}

export function TrialTable({ onApply }: Props) {
  const trials = useTuningStore((s) => s.trials)

  if (trials.length === 0) {
    return null
  }

  const paramNames = Object.keys(trials[0].params)
  const objectiveNames = trials[0].objectives

  return (
    <div className="glass rounded-xl p-4 overflow-auto">
      <h3 className="text-sm font-medium mb-3">Trials</h3>
      <table className="w-full text-xs">
        <thead>
          <tr className="border-b border-border">
            <th className="text-left py-2 px-2 text-muted-foreground font-medium">#</th>
            {objectiveNames.map((name) => (
              <th key={name} className="text-left py-2 px-2 text-muted-foreground font-medium">
                {name}
              </th>
            ))}
            {paramNames.map((name) => (
              <th key={name} className="text-left py-2 px-2 text-muted-foreground font-medium">
                {name}
              </th>
            ))}
            {onApply && <th className="py-2 px-2" />}
          </tr>
        </thead>
        <tbody>
          {trials.map((trial) => (
            <tr key={trial.trial_number} className="border-b border-border/50 hover:bg-zinc-800/50">
              <td className="py-1.5 px-2">{trial.trial_number + 1}</td>
              {trial.values.map((v, i) => (
                <td key={i} className="py-1.5 px-2 tabular-nums">
                  {v.toFixed(4)}
                </td>
              ))}
              {paramNames.map((name) => (
                <td key={name} className="py-1.5 px-2 tabular-nums">
                  {typeof trial.params[name] === 'number'
                    ? trial.params[name].toFixed(4)
                    : trial.params[name]}
                </td>
              ))}
              {onApply && (
                <td className="py-1.5 px-2">
                  <button
                    onClick={() => onApply(trial.params)}
                    className="text-primary hover:text-primary/80 text-[10px]"
                  >
                    Apply
                  </button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
