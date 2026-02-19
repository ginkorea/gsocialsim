import { useCallback, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Play, Activity, BarChart3, FlaskConical } from 'lucide-react'
import { Header } from '@/components/layout/Header'
import { RunCard } from '@/components/simulation/RunCard'
import type { RunInfo } from '@/lib/types'
import { api } from '@/lib/api'

export function Dashboard() {
  const navigate = useNavigate()
  const [runs, setRuns] = useState<RunInfo[]>([])
  const [healthy, setHealthy] = useState<boolean | null>(null)

  const loadRuns = useCallback(async () => {
    try {
      const list = await api.listRuns()
      setRuns(list)
    } catch {
      // ignore
    }
  }, [])

  useEffect(() => {
    api.health().then(() => setHealthy(true)).catch(() => setHealthy(false))
    loadRuns()
  }, [loadRuns])

  const activeRuns = runs.filter((r) => r.status === 'running')
  const recentRuns = runs.slice(0, 6)

  return (
    <div className="flex flex-col h-full">
      <Header title="Dashboard" />
      <div className="flex-1 p-6 space-y-6 overflow-auto">
        {/* Status banner */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-xl p-4 flex items-center justify-between"
        >
          <div>
            <h2 className="text-lg font-semibold">gsocialsim Control Panel</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Configure simulations, watch them run live, and optimize parameters
            </p>
          </div>
          <div className="flex items-center gap-2">
            <div className={`w-2.5 h-2.5 rounded-full ${healthy ? 'bg-green-500' : healthy === false ? 'bg-red-500' : 'bg-yellow-500 animate-pulse'}`} />
            <span className="text-xs text-muted-foreground">
              {healthy ? 'Backend connected' : healthy === false ? 'Backend offline' : 'Connecting...'}
            </span>
          </div>
        </motion.div>

        {/* Quick stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <motion.button
            onClick={() => navigate('/simulate')}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="glass glass-hover rounded-xl p-5 text-left transition-all duration-200"
          >
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-lg bg-green-500/10 flex items-center justify-center">
                <Play className="w-5 h-5 text-green-500" />
              </div>
              <div>
                <div className="text-2xl font-bold">{activeRuns.length}</div>
                <div className="text-xs text-muted-foreground">Active simulations</div>
              </div>
            </div>
          </motion.button>

          <motion.button
            onClick={() => navigate('/results')}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass glass-hover rounded-xl p-5 text-left transition-all duration-200"
          >
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-blue-500" />
              </div>
              <div>
                <div className="text-2xl font-bold">{runs.length}</div>
                <div className="text-xs text-muted-foreground">Total runs</div>
              </div>
            </div>
          </motion.button>

          <motion.button
            onClick={() => navigate('/tune')}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="glass glass-hover rounded-xl p-5 text-left transition-all duration-200"
          >
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center">
                <FlaskConical className="w-5 h-5 text-purple-500" />
              </div>
              <div>
                <div className="text-2xl font-bold">
                  <Activity className="w-5 h-5 inline text-muted-foreground" />
                </div>
                <div className="text-xs text-muted-foreground">Hypertuning</div>
              </div>
            </div>
          </motion.button>
        </div>

        {/* Quick launch */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <button
            onClick={() => navigate('/config')}
            className="w-full glass glass-hover rounded-xl p-6 text-center transition-all duration-200
              border-2 border-dashed border-zinc-700 hover:border-primary/50"
          >
            <Play className="w-8 h-8 text-primary mx-auto mb-2" />
            <div className="text-sm font-medium">Configure & Launch New Simulation</div>
            <div className="text-xs text-muted-foreground mt-1">
              Set parameters, choose a preset, and start a run
            </div>
          </button>
        </motion.div>

        {/* Recent runs */}
        {recentRuns.length > 0 && (
          <div>
            <h3 className="text-sm font-medium mb-3">Recent Runs</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {recentRuns.map((run) => (
                <RunCard key={run.id} run={run} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
