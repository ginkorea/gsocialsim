import { useEffect, useRef, useState } from 'react'
import { ChevronDown, ChevronRight, Terminal } from 'lucide-react'
import { useRunStore } from '@/stores/runStore'

export function LogPanel() {
  const logs = useRunStore((s) => s.logs)
  const [open, setOpen] = useState(true)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (open) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs, open])

  return (
    <div className="glass rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-zinc-700/30 transition-colors"
      >
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-primary" />
          <span className="text-sm font-medium">Simulation Log</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground">{logs.length} entries</span>
          {open ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </div>
      </button>
      {open && (
        <div className="px-4 pb-3 max-h-64 overflow-y-auto font-mono text-xs">
          {logs.length === 0 ? (
            <div className="text-muted-foreground py-2">No log entries yet</div>
          ) : (
            logs.map((line, i) => (
              <div
                key={i}
                className={`py-0.5 ${
                  line.includes('ERROR') ? 'text-red-400' :
                  line.includes('WARNING') ? 'text-amber-400' :
                  line.includes('complete') || line.includes('Complete') ? 'text-green-400' :
                  'text-muted-foreground'
                }`}
              >
                {line}
              </div>
            ))
          )}
          <div ref={bottomRef} />
        </div>
      )}
    </div>
  )
}
