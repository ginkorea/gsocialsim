const SAMPLERS = [
  { id: 'tpe', label: 'TPE', desc: 'Tree-structured Parzen Estimator (recommended)' },
  { id: 'cmaes', label: 'CMA-ES', desc: 'Covariance Matrix Adaptation' },
  { id: 'random', label: 'Random', desc: 'Random search baseline' },
]

interface Props {
  sampler: string
  nTrials: number
  onSamplerChange: (s: string) => void
  onTrialsChange: (n: number) => void
}

export function StrategyPicker({ sampler, nTrials, onSamplerChange, onTrialsChange }: Props) {
  return (
    <div className="space-y-3">
      <h3 className="text-sm font-medium">Strategy</h3>
      <div className="glass rounded-lg p-3 space-y-3">
        <div className="flex gap-2">
          {SAMPLERS.map((s) => (
            <button
              key={s.id}
              onClick={() => onSamplerChange(s.id)}
              className={`flex-1 px-3 py-2 text-xs rounded-lg border transition-all ${
                sampler === s.id
                  ? 'bg-primary/15 border-primary text-primary'
                  : 'border-border text-muted-foreground hover:border-zinc-500'
              }`}
            >
              <div className="font-medium">{s.label}</div>
              <div className="mt-0.5 text-[10px] opacity-70">{s.desc}</div>
            </button>
          ))}
        </div>
        <div className="flex items-center gap-3">
          <label className="text-xs text-muted-foreground">Trials</label>
          <input
            type="number"
            value={nTrials}
            onChange={(e) => onTrialsChange(parseInt(e.target.value) || 10)}
            min={1}
            max={1000}
            className="w-20 px-2 py-1 text-sm bg-zinc-800 border border-border rounded-md"
          />
        </div>
      </div>
    </div>
  )
}
