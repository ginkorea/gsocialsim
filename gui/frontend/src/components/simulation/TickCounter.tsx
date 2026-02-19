import { motion } from 'framer-motion'
import { useRunStore } from '@/stores/runStore'

export function TickCounter() {
  const { currentTick, status } = useRunStore()
  const tick = currentTick?.tick ?? 0
  const total = currentTick?.total ?? 1
  const progress = total > 0 ? tick / total : 0
  const circumference = 2 * Math.PI * 45

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative w-28 h-28">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" fill="none" stroke="#27272a" strokeWidth="4" />
          <motion.circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="#3b82f6"
            strokeWidth="4"
            strokeLinecap="round"
            strokeDasharray={circumference}
            animate={{ strokeDashoffset: circumference * (1 - progress) }}
            transition={{ duration: 0.3 }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            className="text-2xl font-bold tabular-nums"
            key={tick}
            initial={{ opacity: 0.5, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.15 }}
          >
            {tick}
          </motion.span>
          <span className="text-xs text-muted-foreground">/ {total}</span>
        </div>
      </div>
      <div className="text-xs text-muted-foreground">
        {status === 'running' ? `${Math.round(progress * 100)}%` : status}
      </div>
    </div>
  )
}
