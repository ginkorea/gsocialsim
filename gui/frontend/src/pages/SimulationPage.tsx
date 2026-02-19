import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Square, Settings2 } from 'lucide-react'
import { Header } from '@/components/layout/Header'
import { LiveView } from '@/components/simulation/LiveView'
import { useRunStore } from '@/stores/runStore'
import { useSimulation } from '@/hooks/useSimulation'

export function SimulationPage() {
  const navigate = useNavigate()
  const { status, activeRunId } = useRunStore()
  const { cancel, connected } = useSimulation()

  return (
    <div className="flex flex-col h-full">
      <Header title="Live Simulation" />
      <div className="flex-1 p-6 overflow-auto">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-5xl mx-auto space-y-6"
        >
          {/* Controls */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {activeRunId && (
                <span className="text-xs text-muted-foreground font-mono">
                  Run: {activeRunId}
                </span>
              )}
              {connected && (
                <span className="flex items-center gap-1 text-xs text-green-500">
                  <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                  Connected
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              {status === 'running' && (
                <button
                  onClick={cancel}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-red-500/10 text-red-400
                    border border-red-500/30 rounded-lg hover:bg-red-500/20 transition-colors"
                >
                  <Square className="w-3 h-3" />
                  Cancel
                </button>
              )}
              <button
                onClick={() => navigate('/config')}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs text-muted-foreground
                  border border-border rounded-lg hover:bg-zinc-800 transition-colors"
              >
                <Settings2 className="w-3 h-3" />
                Configure
              </button>
            </div>
          </div>

          {/* Live view */}
          {status === 'idle' && !activeRunId ? (
            <div className="glass rounded-xl p-12 text-center">
              <h3 className="text-lg font-medium mb-2">No active simulation</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Configure parameters and start a simulation to see live results
              </p>
              <button
                onClick={() => navigate('/config')}
                className="px-4 py-2 text-sm bg-primary text-white rounded-lg hover:bg-primary/80"
              >
                Go to Configuration
              </button>
            </div>
          ) : (
            <LiveView />
          )}

          {status === 'completed' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass rounded-xl p-4 border border-blue-500/30"
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-blue-400">Simulation complete</span>
                <button
                  onClick={() => navigate('/results')}
                  className="px-3 py-1.5 text-xs bg-blue-500/10 text-blue-400 rounded-lg hover:bg-blue-500/20"
                >
                  View Results
                </button>
              </div>
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  )
}
