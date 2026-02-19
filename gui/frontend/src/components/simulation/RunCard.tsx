import { cn } from '@/lib/utils'
import type { RunInfo } from '@/lib/types'
import { Play, CheckCircle, XCircle, Clock, Ban } from 'lucide-react'

const statusConfig = {
  pending: { icon: Clock, color: 'text-yellow-500', bg: 'bg-yellow-500/10' },
  running: { icon: Play, color: 'text-green-500', bg: 'bg-green-500/10' },
  completed: { icon: CheckCircle, color: 'text-blue-500', bg: 'bg-blue-500/10' },
  failed: { icon: XCircle, color: 'text-red-500', bg: 'bg-red-500/10' },
  cancelled: { icon: Ban, color: 'text-zinc-500', bg: 'bg-zinc-500/10' },
}

export function RunCard({ run }: { run: RunInfo }) {
  const { icon: StatusIcon, color, bg } = statusConfig[run.status]

  return (
    <div className="glass glass-hover rounded-xl p-4 transition-all duration-200 cursor-pointer">
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="text-sm font-medium">{run.id}</div>
          <div className="text-xs text-muted-foreground">
            {run.config?.agents ?? '?'} agents, {run.config?.ticks ?? '?'} ticks
          </div>
        </div>
        <div className={cn('flex items-center gap-1 px-2 py-0.5 rounded-full text-xs', bg, color)}>
          <StatusIcon className="w-3 h-3" />
          {run.status}
        </div>
      </div>
      {run.status === 'running' && (
        <div className="w-full bg-zinc-700 rounded-full h-1.5">
          <div
            className="bg-primary h-full rounded-full transition-all"
            style={{
              width: `${run.total_ticks > 0 ? (run.ticks_completed / run.total_ticks) * 100 : 0}%`,
            }}
          />
        </div>
      )}
      {run.metrics && Object.keys(run.metrics).length > 0 && (
        <div className="mt-2 flex gap-4 text-xs text-muted-foreground">
          {run.metrics.polarization !== undefined && (
            <span>Pol: {Number(run.metrics.polarization).toFixed(3)}</span>
          )}
          {run.metrics.total_impressions !== undefined && (
            <span>Imp: {run.metrics.total_impressions}</span>
          )}
        </div>
      )}
    </div>
  )
}
