import { useCallback, useState } from 'react'
import { useConfigStore } from '@/stores/configStore'
import type { SimulationConfig } from '@/lib/types'

export function JsonEditor() {
  const { config, setConfig } = useConfigStore()
  const [text, setText] = useState(JSON.stringify(config, null, 2))
  const [error, setError] = useState('')

  const handleApply = useCallback(() => {
    try {
      const parsed = JSON.parse(text) as SimulationConfig
      setConfig(parsed)
      setError('')
    } catch (e) {
      setError(String(e))
    }
  }, [text, setConfig])

  return (
    <div className="flex flex-col h-full">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="flex-1 p-4 text-sm font-mono bg-zinc-900 border border-border rounded-lg resize-none
          focus:outline-none focus:ring-1 focus:ring-primary"
        spellCheck={false}
      />
      {error && <p className="text-xs text-destructive mt-1">{error}</p>}
      <button
        onClick={handleApply}
        className="mt-2 self-end px-4 py-2 text-sm bg-primary text-white rounded-lg hover:bg-primary/80 transition-colors"
      >
        Apply JSON
      </button>
    </div>
  )
}
