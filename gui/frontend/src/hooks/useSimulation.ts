import { useCallback, useState } from 'react'
import type { SimulationConfig, WsMessage } from '@/lib/types'
import { api } from '@/lib/api'
import { useRunStore } from '@/stores/runStore'
import { useWebSocket } from './useWebSocket'

export function useSimulation() {
  const { activeRunId, startRun, addTick, complete } = useRunStore()
  const [wsUrl, setWsUrl] = useState<string | null>(null)

  const onMessage = useCallback(
    (data: unknown) => {
      const msg = data as WsMessage
      if (msg.type === 'tick' && msg.data) {
        addTick(msg.data)
      } else if (msg.type === 'complete' && msg.metrics) {
        complete(msg.metrics)
      }
    },
    [addTick, complete]
  )

  const { connected } = useWebSocket(wsUrl, { onMessage })

  const launch = useCallback(
    async (config: SimulationConfig) => {
      const run = await api.createRun(config)
      startRun(run.id)
      setWsUrl(`/ws/run/${run.id}`)
      return run
    },
    [startRun]
  )

  const cancel = useCallback(async () => {
    if (activeRunId) {
      await api.cancelRun(activeRunId)
    }
  }, [activeRunId])

  return { launch, cancel, connected, activeRunId }
}
