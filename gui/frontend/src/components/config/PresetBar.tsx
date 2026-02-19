import { useCallback, useEffect, useState } from 'react'
import { Save, FolderOpen } from 'lucide-react'
import type { Preset, SimulationConfig } from '@/lib/types'
import { api } from '@/lib/api'
import { useConfigStore } from '@/stores/configStore'

export function PresetBar() {
  const [presets, setPresets] = useState<Preset[]>([])
  const [saveName, setSaveName] = useState('')
  const [showSave, setShowSave] = useState(false)
  const { config, setConfig } = useConfigStore()

  const loadPresets = useCallback(async () => {
    try {
      const list = await api.listPresets()
      setPresets(list)
    } catch {
      // ignore
    }
  }, [])

  useEffect(() => {
    loadPresets()
  }, [loadPresets])

  const handleSave = useCallback(async () => {
    if (!saveName.trim()) return
    await api.createPreset(saveName, config)
    setSaveName('')
    setShowSave(false)
    loadPresets()
  }, [saveName, config, loadPresets])

  const handleLoad = useCallback(
    async (id: string) => {
      const preset = await api.getPreset(id)
      setConfig(preset.config as SimulationConfig)
    },
    [setConfig]
  )

  return (
    <div className="flex items-center gap-2 flex-wrap">
      <div className="flex items-center gap-1">
        <FolderOpen className="w-4 h-4 text-muted-foreground" />
        <select
          className="text-sm bg-zinc-800 border border-border rounded-md px-2 py-1 cursor-pointer
            focus:outline-none focus:ring-1 focus:ring-primary"
          onChange={(e) => e.target.value && handleLoad(e.target.value)}
          defaultValue=""
        >
          <option value="" disabled>
            Load preset...
          </option>
          {presets.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
      </div>
      {showSave ? (
        <div className="flex items-center gap-1">
          <input
            type="text"
            placeholder="Preset name"
            value={saveName}
            onChange={(e) => setSaveName(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSave()}
            className="text-sm bg-zinc-800 border border-border rounded-md px-2 py-1
              focus:outline-none focus:ring-1 focus:ring-primary"
          />
          <button
            onClick={handleSave}
            className="px-2 py-1 text-xs bg-primary text-white rounded-md hover:bg-primary/80"
          >
            Save
          </button>
          <button
            onClick={() => setShowSave(false)}
            className="px-2 py-1 text-xs text-muted-foreground hover:text-foreground"
          >
            Cancel
          </button>
        </div>
      ) : (
        <button
          onClick={() => setShowSave(true)}
          className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors"
        >
          <Save className="w-3.5 h-3.5" />
          Save preset
        </button>
      )}
    </div>
  )
}
