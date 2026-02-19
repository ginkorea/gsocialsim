import { useCallback, useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Header } from '@/components/layout/Header'
import { RunComparison } from '@/components/results/RunComparison'
import { ParamDiff } from '@/components/results/ParamDiff'
import { ExportDialog } from '@/components/results/ExportDialog'
import { RunCard } from '@/components/simulation/RunCard'
import type { RunInfo } from '@/lib/types'
import { api } from '@/lib/api'

export function ResultsPage() {
  const [runs, setRuns] = useState<RunInfo[]>([])
  const [selected, setSelected] = useState<Set<string>>(new Set())

  const loadRuns = useCallback(async () => {
    try {
      const list = await api.listRuns()
      setRuns(list)
    } catch {
      // ignore
    }
  }, [])

  useEffect(() => {
    loadRuns()
  }, [loadRuns])

  const toggleSelect = useCallback((id: string) => {
    setSelected((prev) => {
      const next = new Set(prev)
      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }
      return next
    })
  }, [])

  const selectedRuns = runs.filter((r) => selected.has(r.id))

  return (
    <div className="flex flex-col h-full">
      <Header title="Results Explorer" />
      <div className="flex-1 p-6 overflow-auto">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-6xl mx-auto space-y-6"
        >
          <div className="flex items-center justify-between">
            <div className="text-sm text-muted-foreground">
              {selected.size > 0 ? `${selected.size} runs selected` : 'Select runs to compare'}
            </div>
            <ExportDialog runs={selectedRuns} />
          </div>

          {/* Run selection */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {runs.map((run) => (
              <div
                key={run.id}
                onClick={() => toggleSelect(run.id)}
                className={`cursor-pointer transition-all duration-200 rounded-xl ${
                  selected.has(run.id) ? 'ring-2 ring-primary' : ''
                }`}
              >
                <RunCard run={run} />
              </div>
            ))}
          </div>

          {runs.length === 0 && (
            <div className="glass rounded-xl p-12 text-center">
              <h3 className="text-lg font-medium mb-2">No runs yet</h3>
              <p className="text-sm text-muted-foreground">
                Complete a simulation to see results here
              </p>
            </div>
          )}

          {/* Comparison */}
          {selectedRuns.length >= 1 && (
            <>
              <RunComparison runs={selectedRuns} />
              {selectedRuns.length >= 2 && <ParamDiff runs={selectedRuns} />}
            </>
          )}
        </motion.div>
      </div>
    </div>
  )
}
