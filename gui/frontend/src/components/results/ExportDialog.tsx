import { useCallback, useState } from 'react'
import { Download } from 'lucide-react'
import type { RunInfo } from '@/lib/types'
import { api } from '@/lib/api'

interface Props {
  runs: RunInfo[]
}

export function ExportDialog({ runs }: Props) {
  const [exporting, setExporting] = useState(false)

  const handleExport = useCallback(
    async (format: 'json' | 'csv') => {
      setExporting(true)
      try {
        const data = await Promise.all(
          runs.map(async (r) => {
            try {
              const results = await api.getResults(r.id)
              return { run_id: r.id, config: r.config, metrics: r.metrics, results }
            } catch {
              return { run_id: r.id, config: r.config, metrics: r.metrics }
            }
          })
        )

        let blob: Blob
        let filename: string

        if (format === 'json') {
          blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
          filename = `gsocialsim_export_${Date.now()}.json`
        } else {
          const headers = ['run_id', ...Object.keys(runs[0]?.metrics || {})]
          const csvRows = [
            headers.join(','),
            ...runs.map((r) =>
              [r.id, ...headers.slice(1).map((h) => r.metrics?.[h] ?? '')].join(',')
            ),
          ]
          blob = new Blob([csvRows.join('\n')], { type: 'text/csv' })
          filename = `gsocialsim_export_${Date.now()}.csv`
        }

        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = filename
        a.click()
        URL.revokeObjectURL(url)
      } finally {
        setExporting(false)
      }
    },
    [runs]
  )

  return (
    <div className="flex items-center gap-2">
      <button
        onClick={() => handleExport('json')}
        disabled={exporting || runs.length === 0}
        className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-zinc-800 border border-border
          rounded-lg hover:bg-zinc-700 transition-colors disabled:opacity-50"
      >
        <Download className="w-3.5 h-3.5" />
        Export JSON
      </button>
      <button
        onClick={() => handleExport('csv')}
        disabled={exporting || runs.length === 0}
        className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-zinc-800 border border-border
          rounded-lg hover:bg-zinc-700 transition-colors disabled:opacity-50"
      >
        <Download className="w-3.5 h-3.5" />
        Export CSV
      </button>
    </div>
  )
}
