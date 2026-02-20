import { useState, useEffect, useRef, useCallback } from 'react'
import { ChevronDown, ChevronRight, Database, Upload, Eye, EyeOff, AlertTriangle } from 'lucide-react'
import type { DataSourceInfo, DataSourceConfig } from '@/lib/types'
import { api } from '@/lib/api'
import { useConfigStore } from '@/stores/configStore'
import { formatNumber } from '@/lib/utils'

export function DataSourcePanel() {
  const [open, setOpen] = useState(true)
  const [sources, setSources] = useState<DataSourceInfo[]>([])
  const [preview, setPreview] = useState<Record<string, string>[] | null>(null)
  const [showPreview, setShowPreview] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [loadingList, setLoadingList] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const { dataSource, dataSourceInfo, setDataSource } = useConfigStore()

  const loadSources = useCallback(async () => {
    setLoadingList(true)
    try {
      const list = await api.listDataSources()
      setSources(list)
    } catch {
      // ignore
    } finally {
      setLoadingList(false)
    }
  }, [])

  useEffect(() => {
    loadSources()
  }, [loadSources])

  const handleSelect = async (filename: string) => {
    if (!filename) {
      setDataSource(null, null)
      setPreview(null)
      setShowPreview(false)
      return
    }
    try {
      const info = await api.getDataSource(filename)
      const ds: DataSourceConfig = { source_type: 'csv', filename }
      setDataSource(ds, info)
      setPreview(null)
      setShowPreview(false)
    } catch {
      // ignore
    }
  }

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    setUploading(true)
    try {
      const info = await api.uploadDataSource(file)
      await loadSources()
      const ds: DataSourceConfig = { source_type: 'csv', filename: info.filename }
      setDataSource(ds, info)
    } catch {
      // ignore
    } finally {
      setUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ''
    }
  }

  const togglePreview = async () => {
    if (showPreview) {
      setShowPreview(false)
      return
    }
    if (!dataSource?.filename) return
    try {
      const rows = await api.previewDataSource(dataSource.filename)
      setPreview(rows)
      setShowPreview(true)
    } catch {
      // ignore
    }
  }

  const formatBytes = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="glass rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-zinc-700/30 transition-colors"
      >
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-primary" />
          <span className="text-sm font-medium">Data Source</span>
        </div>
        <div className="flex items-center gap-2">
          {dataSource?.filename ? (
            <span className="text-xs text-green-400">{dataSource.filename}</span>
          ) : (
            <span className="text-xs text-amber-400">Not configured</span>
          )}
          {open ? (
            <ChevronDown className="w-4 h-4" />
          ) : (
            <ChevronRight className="w-4 h-4" />
          )}
        </div>
      </button>

      {open && (
        <div className="px-4 pb-4 space-y-3">
          {/* Warning when no data source */}
          {!dataSource?.filename && (
            <div className="flex items-start gap-2 p-3 rounded-lg bg-amber-500/10 border border-amber-500/30">
              <AlertTriangle className="w-4 h-4 text-amber-400 mt-0.5 shrink-0" />
              <p className="text-xs text-amber-400">
                No stimuli data configured. The simulation will run without external information
                sources, which may produce limited results.
              </p>
            </div>
          )}

          {/* Source type selector */}
          <div>
            <label className="text-xs text-muted-foreground mb-1 block">Source Type</label>
            <select
              className="w-full px-3 py-1.5 text-sm bg-zinc-800 border border-border rounded-md
                text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
              value="csv"
              disabled
            >
              <option value="csv">CSV File</option>
              <option value="gdelt" disabled>GDELT (coming soon)</option>
            </select>
          </div>

          {/* File selector */}
          <div>
            <label className="text-xs text-muted-foreground mb-1 block">Stimuli File</label>
            <select
              className="w-full px-3 py-1.5 text-sm bg-zinc-800 border border-border rounded-md
                text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
              value={dataSource?.filename ?? ''}
              onChange={(e) => handleSelect(e.target.value)}
            >
              <option value="">-- None --</option>
              {sources.map((s) => (
                <option key={s.filename} value={s.filename}>
                  {s.filename} ({formatNumber(s.row_count)} rows, ticks {s.tick_min}-{s.tick_max})
                </option>
              ))}
            </select>
            {loadingList && (
              <p className="text-xs text-muted-foreground mt-1">Loading...</p>
            )}
          </div>

          {/* Upload */}
          <div className="flex items-center gap-2">
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv"
              onChange={handleUpload}
              className="hidden"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs
                border border-border rounded-lg hover:bg-zinc-800 transition-colors
                text-muted-foreground hover:text-foreground disabled:opacity-50"
            >
              <Upload className="w-3 h-3" />
              {uploading ? 'Uploading...' : 'Upload CSV'}
            </button>
          </div>

          {/* Info card */}
          {dataSourceInfo && (
            <div className="p-3 rounded-lg bg-zinc-800/50 border border-zinc-700/50 space-y-2">
              <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs">
                <div className="text-muted-foreground">Rows</div>
                <div>{formatNumber(dataSourceInfo.row_count)}</div>
                <div className="text-muted-foreground">Tick Range</div>
                <div>{dataSourceInfo.tick_min} - {dataSourceInfo.tick_max}</div>
                <div className="text-muted-foreground">File Size</div>
                <div>{formatBytes(dataSourceInfo.size_bytes)}</div>
              </div>
              <div>
                <span className="text-xs text-muted-foreground">Columns: </span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {dataSourceInfo.columns.map((col) => (
                    <span
                      key={col}
                      className="px-1.5 py-0.5 text-[10px] bg-zinc-700/50 rounded text-muted-foreground"
                    >
                      {col}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Preview toggle */}
          {dataSourceInfo && (
            <>
              <button
                onClick={togglePreview}
                className="flex items-center gap-1.5 text-xs text-muted-foreground
                  hover:text-foreground transition-colors"
              >
                {showPreview ? <EyeOff className="w-3 h-3" /> : <Eye className="w-3 h-3" />}
                {showPreview ? 'Hide Preview' : 'Show Preview'}
              </button>

              {showPreview && preview && (
                <div className="overflow-x-auto rounded-lg border border-zinc-700/50">
                  <table className="w-full text-xs">
                    <thead>
                      <tr className="bg-zinc-800/80">
                        {dataSourceInfo.columns.map((col) => (
                          <th key={col} className="px-2 py-1.5 text-left text-muted-foreground font-medium whitespace-nowrap">
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {preview.map((row, i) => (
                        <tr key={i} className="border-t border-zinc-700/30">
                          {dataSourceInfo.columns.map((col) => (
                            <td key={col} className="px-2 py-1 whitespace-nowrap max-w-[200px] truncate">
                              {row[col] ?? ''}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  )
}
