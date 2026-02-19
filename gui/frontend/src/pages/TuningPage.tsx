import { useState } from 'react'
import { motion } from 'framer-motion'
import { Play } from 'lucide-react'
import { Header } from '@/components/layout/Header'
import { SearchSpaceEditor } from '@/components/tuning/SearchSpaceEditor'
import { ObjectiveSelector } from '@/components/tuning/ObjectiveSelector'
import { StrategyPicker } from '@/components/tuning/StrategyPicker'
import { OptProgress } from '@/components/tuning/OptProgress'
import { ImportanceChart } from '@/components/tuning/ImportanceChart'
import { TrialTable } from '@/components/tuning/TrialTable'
import { useConfigStore } from '@/stores/configStore'
import { useTuningStore } from '@/stores/tuningStore'
import { useTuning } from '@/hooks/useTuning'

interface SearchSpaceEntry {
  enabled: boolean
  low: number
  high: number
  type: string
}

export function TuningPage() {
  const { config, updateParam } = useConfigStore()
  const { status, bestParams } = useTuningStore()
  const { launch } = useTuning()

  const [space, setSpace] = useState<Record<string, SearchSpaceEntry>>({})
  const [objectives, setObjectives] = useState([{ name: 'polarization', direction: 'minimize' }])
  const [sampler, setSampler] = useState('tpe')
  const [nTrials, setNTrials] = useState(20)

  const handleStart = async () => {
    const searchSpace: Record<string, { type: string; low: number; high: number }> = {}
    for (const [name, entry] of Object.entries(space)) {
      searchSpace[name] = { type: entry.type, low: entry.low, high: entry.high }
    }

    await launch({
      name: `study_${Date.now()}`,
      base_config: config,
      search_space: searchSpace,
      objectives,
      sampler,
      n_trials: nTrials,
      n_parallel: 1,
    })
  }

  const handleApplyParams = (params: Record<string, number>) => {
    for (const [name, value] of Object.entries(params)) {
      updateParam(name, value)
    }
  }

  const canStart = Object.keys(space).length > 0 && objectives.length > 0 && status !== 'running'

  return (
    <div className="flex flex-col h-full">
      <Header title="Hyperparameter Tuning" />
      <div className="flex-1 p-6 overflow-auto">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-6xl mx-auto"
        >
          {status === 'idle' ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="space-y-4">
                <SearchSpaceEditor space={space} onChange={setSpace} />
              </div>
              <div className="space-y-4">
                <ObjectiveSelector objectives={objectives} onChange={setObjectives} />
                <StrategyPicker
                  sampler={sampler}
                  nTrials={nTrials}
                  onSamplerChange={setSampler}
                  onTrialsChange={setNTrials}
                />
                <button
                  onClick={handleStart}
                  disabled={!canStart}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium
                    bg-primary text-white rounded-lg hover:bg-primary/80 transition-colors
                    disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary/20"
                >
                  <Play className="w-4 h-4" />
                  Start Study ({nTrials} trials, {Object.keys(space).length} params)
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              <OptProgress />
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <ImportanceChart importance={bestParams} />
                <div className="glass rounded-xl p-4">
                  <h3 className="text-sm font-medium mb-3">Best Parameters</h3>
                  {Object.keys(bestParams).length > 0 ? (
                    <div className="space-y-1">
                      {Object.entries(bestParams).map(([name, value]) => (
                        <div key={name} className="flex justify-between text-xs">
                          <span className="text-muted-foreground">{name}</span>
                          <span className="tabular-nums">{typeof value === 'number' ? value.toFixed(4) : value}</span>
                        </div>
                      ))}
                      <button
                        onClick={() => handleApplyParams(bestParams)}
                        className="mt-3 w-full px-3 py-1.5 text-xs bg-primary/10 text-primary
                          border border-primary/30 rounded-lg hover:bg-primary/20"
                      >
                        Apply best to config
                      </button>
                    </div>
                  ) : (
                    <div className="text-xs text-muted-foreground">Waiting for results...</div>
                  )}
                </div>
              </div>
              <TrialTable onApply={handleApplyParams} />
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}
