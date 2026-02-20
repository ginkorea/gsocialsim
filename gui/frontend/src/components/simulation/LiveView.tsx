import { TickCounter } from './TickCounter'
import { BeliefChart } from './BeliefChart'
import { MetricsPanel } from './MetricsPanel'
import { LogPanel } from './LogPanel'

export function LiveView() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col lg:flex-row gap-6">
        <div className="lg:w-1/4 flex justify-center">
          <TickCounter />
        </div>
        <div className="lg:w-3/4">
          <MetricsPanel />
        </div>
      </div>
      <BeliefChart />
      <LogPanel />
    </div>
  )
}
