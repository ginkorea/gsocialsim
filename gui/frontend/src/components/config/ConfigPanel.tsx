import { useCallback } from 'react'
import { useConfigStore } from '@/stores/configStore'
import { useParams } from '@/hooks/useParams'
import { ParamGroup } from './ParamGroup'

export function ConfigPanel() {
  const { schema } = useParams()
  const { config, updateParam } = useConfigStore()

  const handleChange = useCallback(
    (name: string, value: number | string | boolean) => {
      updateParam(name, value)
    },
    [updateParam]
  )

  if (!schema) {
    return (
      <div className="flex items-center justify-center h-64 text-muted-foreground text-sm">
        Loading parameter schema...
      </div>
    )
  }

  // Build a flat values map from config
  const values: Record<string, number | string | boolean> = {
    ticks: config.ticks,
    agents: config.agents,
    seed: config.seed,
    network_mode: config.network_mode,
    avg_following: config.avg_following,
    analytics_mode: config.analytics_mode,
    ...config.influence_dynamics,
    ...config.kernel,
    ...config.feed_queue,
    ...config.broadcast_feed,
    ...config.media_diet,
  }

  return (
    <div className="space-y-3">
      {Object.entries(schema.groups).map(([name, params]) => (
        <ParamGroup
          key={name}
          name={name}
          params={params}
          values={values}
          onChange={handleChange}
        />
      ))}
    </div>
  )
}
