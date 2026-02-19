import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Play, Code } from 'lucide-react'
import { Header } from '@/components/layout/Header'
import { ConfigPanel } from '@/components/config/ConfigPanel'
import { PresetBar } from '@/components/config/PresetBar'
import { JsonEditor } from '@/components/config/JsonEditor'
import { useConfigStore } from '@/stores/configStore'
import { useSimulation } from '@/hooks/useSimulation'

export function ConfigPage() {
  const navigate = useNavigate()
  const [tab, setTab] = useState<'visual' | 'json'>('visual')
  const { config, dirty, resetToDefaults } = useConfigStore()
  const { launch } = useSimulation()

  const handleStart = async () => {
    await launch(config)
    navigate('/simulate')
  }

  return (
    <div className="flex flex-col h-full">
      <Header title="Configure Simulation" />
      <div className="flex-1 p-6 overflow-auto">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl mx-auto space-y-4"
        >
          {/* Top bar */}
          <div className="flex items-center justify-between flex-wrap gap-3">
            <PresetBar />
            <div className="flex items-center gap-2">
              <button
                onClick={resetToDefaults}
                className="px-3 py-1.5 text-xs text-muted-foreground hover:text-foreground
                  border border-border rounded-lg hover:bg-zinc-800 transition-colors"
              >
                Reset defaults
              </button>
              <button
                onClick={handleStart}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-primary text-white
                  rounded-lg hover:bg-primary/80 transition-colors shadow-lg shadow-primary/20"
              >
                <Play className="w-4 h-4" />
                Start Simulation
              </button>
            </div>
          </div>

          {/* Tab switcher */}
          <div className="flex items-center gap-1 p-1 bg-zinc-800/50 rounded-lg w-fit">
            <button
              onClick={() => setTab('visual')}
              className={`px-3 py-1.5 text-xs rounded-md transition-colors ${
                tab === 'visual' ? 'bg-zinc-700 text-foreground' : 'text-muted-foreground'
              }`}
            >
              Visual Editor
            </button>
            <button
              onClick={() => setTab('json')}
              className={`flex items-center gap-1 px-3 py-1.5 text-xs rounded-md transition-colors ${
                tab === 'json' ? 'bg-zinc-700 text-foreground' : 'text-muted-foreground'
              }`}
            >
              <Code className="w-3 h-3" />
              JSON
            </button>
          </div>

          {/* Editor content */}
          {tab === 'visual' ? <ConfigPanel /> : <JsonEditor />}

          {dirty && (
            <div className="text-xs text-yellow-500">
              Configuration has unsaved changes
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}
