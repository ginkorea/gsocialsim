import { motion } from 'framer-motion'
import { useRunStore } from '@/stores/runStore'
import { formatNumber, polarizationLabel } from '@/lib/utils'
import { Eye, MousePointerClick, Zap, BarChart3 } from 'lucide-react'

function MetricCard({
  icon: Icon,
  label,
  value,
  subtext,
}: {
  icon: typeof Eye
  label: string
  value: string
  subtext?: string
}) {
  return (
    <div className="glass rounded-lg p-3">
      <div className="flex items-center gap-2 mb-1">
        <Icon className="w-4 h-4 text-primary" />
        <span className="text-xs text-muted-foreground">{label}</span>
      </div>
      <motion.div
        className="text-xl font-bold tabular-nums"
        key={value}
        initial={{ opacity: 0.5 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2 }}
      >
        {value}
      </motion.div>
      {subtext && <span className="text-xs text-muted-foreground">{subtext}</span>}
    </div>
  )
}

export function MetricsPanel() {
  const { currentTick, tickHistory } = useRunStore()

  const impressions = currentTick?.impressions ?? 0
  const consumed = currentTick?.consumed ?? 0
  const deltas = currentTick?.belief_deltas ?? 0
  const leans = currentTick?.leans ?? []

  // Calculate polarization (variance of leans)
  const polarization = leans.length > 0
    ? leans.reduce((sum, l) => sum + l * l, 0) / leans.length -
      Math.pow(leans.reduce((sum, l) => sum + l, 0) / leans.length, 2)
    : 0

  return (
    <div className="grid grid-cols-2 gap-3">
      <MetricCard
        icon={Eye}
        label="Impressions"
        value={formatNumber(impressions)}
        subtext="total"
      />
      <MetricCard
        icon={MousePointerClick}
        label="Consumed"
        value={formatNumber(consumed)}
        subtext={impressions > 0 ? `${Math.round((consumed / impressions) * 100)}% rate` : ''}
      />
      <MetricCard
        icon={Zap}
        label="Belief Deltas"
        value={formatNumber(deltas)}
        subtext={`${tickHistory.length} ticks`}
      />
      <MetricCard
        icon={BarChart3}
        label="Polarization"
        value={polarization.toFixed(3)}
        subtext={polarizationLabel(polarization)}
      />
    </div>
  )
}
