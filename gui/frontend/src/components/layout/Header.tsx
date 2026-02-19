import { useRunStore } from '@/stores/runStore'
import { cn } from '@/lib/utils'

export function Header({ title }: { title: string }) {
  const status = useRunStore((s) => s.status)

  return (
    <header className="h-14 border-b border-border flex items-center justify-between px-6 bg-card/30 backdrop-blur-sm">
      <h1 className="text-lg font-semibold tracking-tight">{title}</h1>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <div
            className={cn(
              'w-2 h-2 rounded-full',
              status === 'running'
                ? 'bg-green-500 animate-pulse'
                : status === 'completed'
                ? 'bg-blue-500'
                : 'bg-zinc-600'
            )}
          />
          {status === 'running'
            ? 'Simulation running'
            : status === 'completed'
            ? 'Completed'
            : 'Idle'}
        </div>
      </div>
    </header>
  )
}
